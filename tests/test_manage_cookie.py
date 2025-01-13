import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Iterable, Iterator
from unittest.mock import MagicMock, patch

import github
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
            GITHUB_API_TOKEN="unittest_token",
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


@pytest.fixture(autouse=True)
def mock_pygithub(new_cookie: Path) -> Iterator[MagicMock]:
    with patch.object(github, "Github") as obj:
        gh = obj.return_value
        gh.get_repo.return_value = SimpleNamespace(
            name=PROJECT_NAME,
            full_name=f"{AUTHOR_NAME}/{PROJECT_NAME}",
            ssh_url=str(new_cookie),
            html_url=str(new_cookie),
            get_pulls=MagicMock(
                return_value=[
                    SimpleNamespace(
                        url="https://unittest.example.com/repo/pulls/1138"
                    )
                ],
            ),
            get_branch=lambda name: SimpleNamespace(name=name),
            get_latest_release=lambda: SimpleNamespace(title="v1.1.38"),
        )
        yield obj


@pytest.fixture
def new_cookie_with_lock(new_cookie: Path, temp_dir: str) -> Iterator[Path]:
    for cmd in (
        ["poetry", "sync"],
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


@pytest.mark.parametrize("add_commit", (True, False))
def test_manage_cookie_release(new_cookie: str, add_commit: bool) -> None:
    subprocess.run(["git", "tag", "v1.1.38", "@"], cwd=new_cookie, check=True)
    if add_commit:
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "create empty commit"],
            cwd=new_cookie,
            check=True,
        )
    _manage_cookie(["manage-cookie", "release", str(new_cookie), "-p"])
