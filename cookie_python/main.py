import argparse
import os
import subprocess
from typing import List, Tuple

TEMPLATE_REPOSITORY_URL = "https://github.com/smkent/cookie-python"


def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "project_dir", help="New project parent directory", type=str
    )
    ap.add_argument(
        "--local",
        "-l",
        action="store_true",
        dest="local_template",
        help=(
            "Create project from local template instead of "
            "template repository URL"
        ),
    )
    return ap.parse_known_args()


def main() -> None:
    args, more_args = parse_args()
    template_path = (
        os.path.dirname(os.path.dirname(__file__))
        if args.local_template
        else TEMPLATE_REPOSITORY_URL
    )
    subprocess.check_call(
        ["cruft", "create", "--output-dir", args.project_dir]
        + more_args
        + [template_path]
    )
