import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterator
from unittest.mock import patch

import pytest

from cookie_python.manage.main import main as manage_cookie_main
from cookie_python.new import main as new_cookie_main


@pytest.fixture
def new_cookie(temp_dir: str) -> Iterator[Path]:
    author_name = "Ness"
    author_email = "ness@onett.example"
    project_name = "unit-test-1"
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
                "author_email": author_email,
                "author_name": author_name,
                "github_user": "ness.unittest.example",
                "project_description": "Unit test project",
                "project_name": project_name,
            }
        ),
        "-c",
        "f2f7eddb101275f2909525e579e0ed6f3b5305fa",
    ]
    with patch.object(sys, "argv", testargs):
        new_cookie_main()
    project_dir = Path(temp_dir) / project_name
    environ = os.environ.copy()
    environ.update(
        dict(
            GIT_AUTHOR_NAME=author_name,
            GIT_AUTHOR_EMAIL=author_email,
            GIT_COMMITTER_NAME=author_name,
            GIT_COMMITTER_EMAIL=author_email,
        )
    )
    for cmd in (
        ["poetry", "lock", "--no-update"],
        ["git", "add", "poetry.lock"],
        ["git", "commit", "-m", "Create `poetry.lock`"],
    ):
        subprocess.run(cmd, cwd=project_dir, check=True, env=environ)
    yield project_dir


def test_manage_cookie_update(new_cookie: str) -> None:
    testargs = ["manage-cookie", "update", str(new_cookie), "-p"]
    with patch.object(sys, "argv", testargs):
        manage_cookie_main()
