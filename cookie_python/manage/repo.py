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
from typing import Any, Optional

import loguru


class RepoSandbox:
    def __init__(self, repo: str, dry_run: bool = False) -> None:
        self._stack = contextlib.ExitStack()
        self.repo = repo
        self.branch = "update-cookie"
        self.dry_run = dry_run

    def __enter__(self) -> RepoSandbox:
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        self._stack.close()

    @cached_property
    def logger(self) -> "loguru.Logger":
        return loguru.logger.bind(repo=self.repo)

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
            ["git", "clone", self.repo, "repo"], cwd=self.tempdir, check=True
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

    def find_existing_pr(self) -> Optional[str]:
        with contextlib.suppress(
            subprocess.CalledProcessError, json.JSONDecodeError, TypeError
        ):
            for pr in json.loads(
                self.run(
                    [
                        "gh",
                        "pr",
                        "list",
                        "-H",
                        self.branch,
                        "-B",
                        "main",
                        "--json",
                        ",".join(("url", "headRefName", "baseRefName")),
                    ],
                    capture_output=True,
                    check=True,
                ).stdout.decode()
            ):
                pr_url = str(pr.pop("url"))
                if pr == {"headRefName": self.branch, "baseRefName": "main"}:
                    return pr_url
        return None

    def close_existing_pr(self) -> None:
        # Locate existing PR
        pr_url = self.find_existing_pr()
        if pr_url:
            if self.dry_run:
                self.logger.info(f"Would close existing PR {pr_url}")
            else:
                self.run(["gh", "pr", "close", pr_url])
                self.logger.info(f"Closed existing PR {pr_url}")
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
        pr_url = self.run(
            [
                "gh",
                "pr",
                "create",
                "--title",
                commit_title.strip(),
                "--body-file",
                "-",
                "--base",
                "main",
                "--head",
                self.branch,
            ],
            input=os.linesep.join(commit_body).encode("utf-8"),
            capture_output=True,
        ).stdout.decode()
        self.logger.success(f"Opened PR {pr_url}")
