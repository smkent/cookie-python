from __future__ import annotations

import argparse
from enum import Enum
from typing import Callable, Optional

from .update import update_action


class Action(str, Enum):
    UPDATE = (
        "update",
        update_action,
        "Update repository cruft and dependencies",
    )

    def __new__(
        cls,
        value: str,
        func: Optional[Callable[[argparse.Namespace], None]] = None,
        description: str = "",
    ) -> Action:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.func = func  # type: ignore
        obj.description = description  # type: ignore
        return obj


def main() -> None:
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
    args.action.func(args)
