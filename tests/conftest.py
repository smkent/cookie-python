import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from unittest.mock import patch

import pytest


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
