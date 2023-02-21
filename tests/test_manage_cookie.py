import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Iterator
from unittest.mock import patch

import pytest

from cookie_python.manage.main import main as manage_cookie_main
from cookie_python.new import main as new_cookie_main

AUTHOR_NAME = "Ness"
AUTHOR_EMAIL = "ness@onett.example"
PROJECT_NAME = "unit-test-1"


@pytest.fixture
def environ() -> Iterator[None]:
    env = os.environ.copy()
    env.update(
        dict(
            GIT_AUTHOR_NAME=AUTHOR_NAME,
            GIT_AUTHOR_EMAIL=AUTHOR_EMAIL,
            GIT_COMMITTER_NAME=AUTHOR_NAME,
            GIT_COMMITTER_EMAIL=AUTHOR_EMAIL,
        )
    )
    with patch.dict(os.environ, env):
        yield


@pytest.fixture(params=["@"])
def new_cookie(
    request: pytest.FixtureRequest, environ: None, temp_dir: str
) -> Iterator[Path]:
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
                "author_email": AUTHOR_EMAIL,
                "author_name": AUTHOR_NAME,
                "github_user": "ness.unittest.example",
                "project_description": "Unit test project",
                "project_name": PROJECT_NAME,
            }
        ),
        "-c",
        request.param,
    ]
    with patch.object(sys, "argv", testargs):
        new_cookie_main()
    yield Path(temp_dir) / PROJECT_NAME


@pytest.fixture
def new_cookie_with_lock(new_cookie: Path, temp_dir: str) -> Iterator[Path]:
    for cmd in (
        ["poetry", "lock", "--no-update"],
        ["git", "add", "poetry.lock"],
        ["git", "commit", "-m", "Create `poetry.lock`"],
    ):
        subprocess.run(cmd, cwd=new_cookie, check=True)
    yield new_cookie


def _manage_cookie(argv: Iterable[str]) -> None:
    with patch.object(sys, "argv", argv):
        manage_cookie_main()


@pytest.mark.parametrize(
    "new_cookie",
    ("@", "f2f7eddb101275f2909525e579e0ed6f3b5305fa"),
    ids=["no_updates", "updates"],
    indirect=True,
)
def test_manage_cookie_update(new_cookie_with_lock: str) -> None:
    _manage_cookie(
        ["manage-cookie", "update", str(new_cookie_with_lock), "-p"]
    )
