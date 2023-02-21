from __future__ import annotations

import contextlib
import os
import subprocess
import tempfile
from functools import cached_property, partial
from pathlib import Path
from types import TracebackType
from typing import Any, Optional


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
        run = partial(subprocess.run, cwd=clone_path, check=True)
        if (
            run(
                ["git", "ls-remote", "origin", self.branch],
                capture_output=True,
            )
            .stdout.decode()  # type: ignore
            .strip()
        ):
            raise Exception(f'Branch "{self.branch}" already exists on remote')
        run(["git", "checkout", "-b", self.branch])
        run(["git", "reset", "--hard", "origin/main"])
        return clone_path

    def run(
        self, *popenargs: Any, check: bool = True, **kwargs: Any
    ) -> subprocess.CompletedProcess:
        kwargs.setdefault("cwd", self.clone_path)
        return subprocess.run(*popenargs, check=check, **kwargs)

    def shell(self) -> None:
        print('Run "exit 1" to abort')
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
            print(e)
            print("Resolve errors and exit shell to continue")
            self.shell()

    def open_pr(self, message: str) -> None:
        if self.dry_run:
            return
        self.run(["git", "push", "origin", self.branch])
        commit_title, _, *commit_body = message.splitlines()
        self.run(
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
        )
