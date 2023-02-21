from __future__ import annotations

import argparse
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

from .repo import RepoSandbox

F = TypeVar("F", bound=Callable[[Any, Path], Optional[str]])
A = TypeVar("A", bound=Callable[[str, argparse.Namespace], None])


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
