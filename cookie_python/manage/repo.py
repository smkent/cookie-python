from __future__ import annotations

import contextlib
import subprocess
import tempfile
from functools import cached_property, partial
from pathlib import Path
from types import TracebackType
from typing import Callable, Optional


class RepoSandbox:
    def __init__(self, repo: str) -> None:
        self._stack = contextlib.ExitStack()
        self.repo = repo
        self.run: Optional[
            Callable[..., subprocess.CompletedProcess[str]]
        ] = None

    @cached_property
    def tempdir(self) -> Path:
        return Path(
            self._stack.enter_context(
                tempfile.TemporaryDirectory(suffix=".manage_cookie")
            )
        )

    def setup_repo(self) -> None:
        subprocess.run(
            ["git", "clone", self.repo, "repo"], cwd=self.tempdir, check=True
        )
        branch = "update-cookie"
        clonepath = self.tempdir / "repo"
        self.run = partial(subprocess.run, cwd=clonepath, check=True)
        if (
            self.run(
                ["git", "ls-remote", "origin", branch],
                capture_output=True,
            )  # type: ignore
            .stdout.decode("utf-8")
            .strip()
        ):
            print(f'Branch "{branch}" already exists on remote')
            return
        self.run(["git", "checkout", "-b", branch])
        self.run(["git", "reset", "--hard", "origin/main"])

    def __enter__(self) -> RepoSandbox:
        self.setup_repo()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        self._stack.close()
