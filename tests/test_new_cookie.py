import json
import os
import subprocess
import sys
import tempfile
from typing import Iterable
from unittest import mock

import pytest

from cookie_python.main import main


@pytest.fixture
def temp_dir() -> Iterable[str]:
    with tempfile.TemporaryDirectory() as td:
        yield os.path.join(td)


def test_new_cookie_create(temp_dir: str) -> None:
    testargs = [
        "new-cookie",
        "--local",
        temp_dir,
        "--",
        "-y",
        "--extra-context",
        json.dumps({"project_name": "unit-test-1"}),
    ]
    with mock.patch.object(sys, "argv", testargs):
        main()
    project_dir = os.path.join(temp_dir, "unit-test-1")
    assert os.path.isdir(project_dir)
    subprocess.check_call(["poetry", "install"], cwd=project_dir)
    subprocess.check_call(
        ["poetry", "run", "cruft", "diff", "--exit-code"], cwd=project_dir
    )
