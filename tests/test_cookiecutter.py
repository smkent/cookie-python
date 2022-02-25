import os
import subprocess
from typing import Any

import yaml


def test_bake_project(cookies: Any) -> None:
    result = cookies.bake(
        extra_context=dict(
            author_name="Ness",
            author_email="pk-fire@onett.example.com",
            project_name="test-baked-cookie",
            project_description=(
                'This is a test project called "test-baked-cookie"'
            ),
        )
    )

    assert result.exit_code == 0
    assert not result.exception

    assert result.project_path.name == "test-baked-cookie"
    assert result.project_path.is_dir()

    assert os.path.isdir(
        os.path.join(result.project_path, "test_baked_cookie")
    )

    # Validate CI configuration
    data = yaml.safe_load(
        open(
            os.path.join(
                result.project_path,
                ".github",
                "workflows",
                "ci.yml",
            ),
            "r",
        )
    )
    assert (
        data["jobs"]["build-test-publish"]["env"]["ENABLE_PYPI_PUBLISH"]
        is False
    )
    assert data["jobs"]["build-test-publish"]["env"]["ENABLE_COVERAGE"] is True

    # Install rendered project
    subprocess.check_call(["poetry", "install"], cwd=result.project_path)

    # Run rendered project's tests
    subprocess.check_call(
        ["poetry", "run", "poe", "test"], cwd=result.project_path
    )
