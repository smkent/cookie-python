from __future__ import annotations

import contextlib
import subprocess
import tempfile
from functools import cached_property, partial
from pathlib import Path
from types import TracebackType
from typing import Any, Optional


class RepoSandbox:
    def __init__(self, repo: str) -> None:
        self._stack = contextlib.ExitStack()
        self.repo = repo
        self.branch = "update-cookie"

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
