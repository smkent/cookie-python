import os
import subprocess
from typing import Any

import yaml


def test_bake_project(cookies: Any) -> None:
    result = cookies.bake(extra_context=dict(project_name="test-baked-cookie"))

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

    # Run rendered project's tests
    subprocess.check_call(
        ["make", "update", "all", "dist"], cwd=result.project_path
    )
