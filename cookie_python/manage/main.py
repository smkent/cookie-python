from __future__ import annotations

import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

from loguru import logger

from .release import release_action
from .update import update_action


class Action(str, Enum):
    UPDATE = (
        "update",
        update_action,
        "Update repository cruft and dependencies",
    )
    RELEASE = (
        "release",
        release_action,
        "Release a new patch version",
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


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        format=(
            f"<b>[{Path(sys.argv[0]).name}]</b>"
            " <light-blue>{time:YYYY-MM-DD HH:mm:ss}</light-blue>"
            " <light-magenta>{extra[repo]}</light-magenta>"
            " <level>{message}</level>"
        ),
    )


def main() -> None:
    configure_logging()
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "action",
        type=Action,
        choices=list(Action),
        metavar="|".join([a.value for a in Action]),
        help="Action to perform ("
        + ", ".join(
            [f"{a.value}: {a.description}" for a in Action]  # type: ignore
        )
        + ")",
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
