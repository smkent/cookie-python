import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from cookie_python.new import main as new_cookie_main

AUTHOR_NAME = "Ness"
AUTHOR_EMAIL = "ness@onett.example"
PROJECT_NAME = "unit-test-1"


@pytest.fixture
def project_environment() -> Iterator[None]:
    add_values = dict(
        GIT_AUTHOR_NAME=AUTHOR_NAME,
        GIT_AUTHOR_EMAIL=AUTHOR_EMAIL,
        GIT_COMMITTER_NAME=AUTHOR_NAME,
        GIT_COMMITTER_EMAIL=AUTHOR_EMAIL,
        GITHUB_API_TOKEN="unittest_token",
    )
    with patch.dict(os.environ, add_values):
        yield


@pytest.fixture(scope="session", autouse=True)
def subprocess_environment() -> Iterator[None]:
    with patch.dict(os.environ, {}) as patched_env:
        if "VIRTUAL_ENV" in patched_env:
            del patched_env["VIRTUAL_ENV"]
        yield


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("cookie", "python-cookie test helpers")
    group.addoption(
        "--update-expected-outputs",
        action="store_true",
        dest="update_expected_outputs",
        help="Update expected test data with generated results",
    )


@pytest.fixture
def opt_update_expected_outputs(request: pytest.FixtureRequest) -> bool:
    value = request.config.getoption("--update-expected-outputs")
    assert isinstance(value, bool)
    return value


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    with TemporaryDirectory(prefix="cookie-python.unittest.") as td:
        yield Path(td)


@pytest.fixture(params=["@"])
def new_cookie(
    request: pytest.FixtureRequest, project_environment: None, temp_dir: Path
) -> Iterator[Path]:
    testargs = [
        "new-cookie",
        "--local",
        str(temp_dir),
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
                "enable_container_publish": "yes",
            }
        ),
        "-c",
        request.param,
    ]
    with patch.object(sys, "argv", testargs):
        new_cookie_main()
    project_dir = temp_dir / PROJECT_NAME
    yield project_dir
    if (project_dir / "pyproject.toml").is_file():
        subprocess.run(["poetry", "env", "remove", "--all"], cwd=project_dir)
