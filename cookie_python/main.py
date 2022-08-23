import argparse
import os
import subprocess
import time
from pathlib import Path
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


def locate_new_project(parent_dir: str) -> str:
    paths = sorted(
        Path(parent_dir).iterdir(), key=os.path.getmtime, reverse=True
    )
    for path in paths:
        if os.path.isfile(os.path.join(parent_dir, path, ".cruft.json")):
            sub_dir = os.path.join(parent_dir, path)
            assert (
                len(
                    subprocess.check_output(
                        ["git", "log", "--oneline"], cwd=sub_dir
                    )
                    .decode("utf-8")
                    .strip()
                    .splitlines()
                )
                == 1
            ), (
                f"Detected project directory {sub_dir} "
                "should have exactly 1 commit"
            )
            assert (
                subprocess.check_output(
                    ["git", "status", "--porcelain=v1"], cwd=sub_dir
                )
                .decode("utf-8")
                .strip()
                == "?? .cruft.json"
            ), f"Detected project directory {sub_dir} has unexpected contents"
            assert (
                time.time() - os.stat(sub_dir).st_ctime < 60
            ), f"Detected project directory {sub_dir} was not created just now"
            return sub_dir
    raise Exception("Unable to locate newly-created project directory")


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
    new_project_dir = locate_new_project(args.project_dir)
    print(new_project_dir)
    subprocess.check_call(["git", "add", ".cruft.json"], cwd=new_project_dir)
    subprocess.check_call(
        ["git", "commit", "--amend", "--no-edit"], cwd=new_project_dir
    )
