import json
import os
import subprocess
import sys
from unittest import mock

from cookie_python.new import main


def test_new_cookie_create(temp_dir: str) -> None:
    testargs = [
        "new-cookie",
        "--local",
        temp_dir,
        "--",
        "-d",
        "-y",
        "--extra-context",
        json.dumps(
            {
                "author_email": "ness@onett.example",
                "author_name": "Ness",
                "github_user": "ness.unittest.example",
                "project_description": "Unit test project",
                "project_name": "unit-test-1",
            }
        ),
    ]
    with mock.patch.object(sys, "argv", testargs):
        main()
    project_dir = os.path.join(temp_dir, "unit-test-1")
    assert os.path.isdir(project_dir)
    assert not (
        subprocess.check_output(
            ["git", "status", "--porcelain=v1"], cwd=project_dir
        )
        .decode("utf-8")
        .strip()
    ), "Untracked files present in template-rendered project"

    subprocess.check_call(
        ["poetry", "run", "cruft", "diff", "--exit-code"], cwd=project_dir
    )
    # Install rendered project
    subprocess.check_call(["poetry", "install"], cwd=project_dir)
    # Run rendered project's tests
    subprocess.check_call(["poetry", "run", "poe", "test"], cwd=project_dir)
