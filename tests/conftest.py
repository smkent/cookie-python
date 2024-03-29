import os
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest


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
def temp_dir() -> Iterator[str]:
    with TemporaryDirectory(prefix="cookie-python.unittest.") as td:
        yield os.path.join(td)
