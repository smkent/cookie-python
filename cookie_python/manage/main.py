from __future__ import annotations

import argparse
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

from .repo import RepoSandbox

F = TypeVar("F", bound=Callable[[Any, Path], Optional[str]])
A = TypeVar("A", bound=Callable[[str, argparse.Namespace], None])


class Action(str, Enum):
    UPDATE = "update", "Update repository cruft and dependencies"

    def __new__(cls, value: str, description: str = "") -> Action:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore
        return obj


class ManageCookie:
    def __init__(self) -> None:
        self.args = self._parse_args()

    @staticmethod
    def _parse_args() -> argparse.Namespace:
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
            with RepoSandbox(repo):
                pass


def main() -> None:
    mc = ManageCookie()
    mc.run()
