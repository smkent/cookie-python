from __future__ import annotations

import argparse
import contextlib
import subprocess
import tempfile
from enum import Enum
from functools import cached_property, partial
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Optional, TypeVar

# import semver

F = TypeVar("F", bound=Callable[[Any, Path], Optional[str]])
A = TypeVar("A", bound=Callable[[str, argparse.Namespace], None])


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


class Action(str, Enum):
    UPDATE = "update", "test"

    def __new__(cls, value: str, description: str = "") -> Action:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore
        return obj


class ManageCookie:
    def __init__(self) -> None:
        self.args = self.parse_args()
        print(self.args)

    def parse_args(self) -> argparse.Namespace:
        ap = argparse.ArgumentParser()
        ap.add_argument(
            "action",
            type=lambda value: Action(str(value)),
            choices=list(Action),
        )
        ap.add_argument("repo", nargs="+", help="Repository URL")
        ap.add_argument(
            "-p",
            "--pretend",
            "--dry-run",
            dest="dry_run",
            action="store_true",
            help="Dry run",
        )
        args = ap.parse_args()
        return args

    def run(self) -> None:
        for repo in self.args.repo:
            with RepoSandbox(repo) as rs:
                print(f"In the sandbox for {repo}")
                print(rs.tempdir)
                print(rs)

    @staticmethod
    def main() -> None:
        print("manage cookie main")
        mc = ManageCookie()
        mc.run()
