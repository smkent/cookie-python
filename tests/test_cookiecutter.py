import os
import subprocess
from typing import Any


def test_bake_project(cookies: Any) -> None:
    result = cookies.bake(extra_context=dict(project_name="test-baked-cookie"))

    assert result.exit_code == 0
    assert not result.exception

    assert result.project_path.name == "test-baked-cookie"
    assert result.project_path.is_dir()

    assert os.path.isdir(
        os.path.join(result.project_path, "test_baked_cookie")
    )

    subprocess.check_call(
        ["make", "update", "all", "dist"], cwd=result.project_path
    )
