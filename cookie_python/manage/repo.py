from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import tempfile
from functools import cached_property
from pathlib import Path
from types import TracebackType
from typing import Any

import loguru

from .github import GithubRepo


class RepoSandbox:
    def __init__(
        self, repo: str, dry_run: bool = False, branch: str = "manage-cookie"
    ) -> None:
        self._stack = contextlib.ExitStack()
        self.repo = self.gh.find_repo(repo)
        self.branch = branch
        self.dry_run = dry_run

    def __enter__(self) -> RepoSandbox:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        self._stack.close()

    @cached_property
    def gh(self) -> GithubRepo:
        return GithubRepo()

    @cached_property
    def latest_release(self) -> str:
        return self.repo.get_latest_release().title

    def create_release(self, tag: str) -> None:
        print(f"Should create release {tag}")
        # PyGithub's repository create_tag_and_release() doesn't support
        # generate_release_notes
        self.repo._requester.requestJsonAndCheck(
            "POST",
            f"/repos/{self.repo.full_name}/releases",
            input={
                "tag_name": tag,
                "generate_release_notes": True,
            },
        )

    @cached_property
    def logger(self) -> loguru.Logger:
        return loguru.logger.bind(repo=self.repo.full_name)

    @cached_property
    def tempdir(self) -> Path:
        return Path(
            self._stack.enter_context(
                tempfile.TemporaryDirectory(suffix=".manage_cookie")
            )
        )

    @cached_property
    def clone_path(self) -> Path:
        subprocess.run(
            ["git", "clone", self.repo.ssh_url, "repo"],
            cwd=self.tempdir,
            check=True,
        )
        clone_path = self.tempdir / "repo"
        for cmd in (
            ["git", "checkout", "-b", self.branch],
            ["git", "reset", "--hard", "origin/main"],
        ):
            subprocess.run(cmd, cwd=clone_path, check=True)
        return clone_path

    def cruft_attr(self, attr: str) -> str:
        with open(self.clone_path / ".cruft.json") as f:
            cruft = json.load(f)
        value = cruft[attr]
        assert isinstance(value, str)
        return value

    def run(
        self, *popenargs: Any, check: bool = True, **kwargs: Any
    ) -> subprocess.CompletedProcess:
        kwargs.setdefault("cwd", self.clone_path)
        kwargs.setdefault("env", os.environ.copy())
        kwargs["env"].setdefault(
            "PYTHON_KEYRING_BACKEND", "keyring.backends.null.Keyring"
        )
        return subprocess.run(*popenargs, check=check, **kwargs)

    def shell(self) -> None:
        if sys.__stdin__.isatty():
            self.logger.info('Starting shell. Run "exit 1" to abort.')
            self.run([os.environ.get("SHELL", "/bin/bash")])

    def commit_changes(self, message: str) -> None:
        self.run(["git", "add", "--", "."])
        self.run(
            ["git", "commit", "--no-verify", "-F", "-"],
            input=message.replace("```\n", "").encode(),
        )
        if self.dry_run:
            self.run(
                [
                    "git",
                    "--no-pager",
                    "show",
                    "--",
                    ".",
                    ":!poetry.lock",
                    ":!.cruft.json",
                ]
            )
        self.lint_test()

    def lint_test(self) -> None:
        self.run(["poetry", "run", "poe", "lint"], check=False)
        with contextlib.suppress(subprocess.CalledProcessError):
            self.run(["git", "add", "--", "."])
            self.run(["git", "commit", "-m", "Apply automatic linting fixes"])
        try:
            self.run(["poetry", "run", "poe", "test"])
        except subprocess.CalledProcessError as e:
            self.logger.error(str(e))
            self.logger.error("Resolve errors and exit shell to continue")
            self.shell()

    def close_existing_pr(self) -> None:
        # Locate existing PR
        pr = self.gh.find_pr(self.repo, self.branch)
        if pr:
            if self.dry_run:
                self.logger.info(f"Would close existing PR {pr.url}")
            else:
                pr.edit(state="closed")
                self.logger.info(f"Closed existing PR {pr.url}")
        if self.dry_run:
            return
        # Delete existing branch
        delete_result = self.run(
            ["git", "push", "origin", f":{self.branch}"],
            capture_output=True,
            check=False,
        )
        if delete_result.returncode == 0:
            self.logger.info(f"Deleted existing remote branch {self.branch}")

    def open_pr(self, message: str) -> None:
        self.close_existing_pr()
        if self.dry_run:
            self.logger.success("Would open PR")
            return
        self.run(["git", "push", "origin", self.branch])
        commit_title, _, *commit_body = message.splitlines()
        pr = self.repo.create_pull(
            base="main",
            head=self.branch,
            title=commit_title.strip(),
            body=os.linesep.join(commit_body),
        )
        self.logger.success(f"Opened PR {pr.html_url}")
