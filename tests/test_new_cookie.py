import os
import subprocess
from pathlib import Path


def test_new_cookie_create(new_cookie: Path, temp_dir: Path) -> None:
    assert os.path.isdir(new_cookie)
    assert not (
        subprocess.check_output(
            ["git", "status", "--porcelain=v1"], cwd=new_cookie
        )
        .decode("utf-8")
        .strip()
    ), "Untracked files present in template-rendered project"

    # Verify cruft is up to date
    subprocess.check_call(
        ["poetry", "run", "cruft", "diff", "--exit-code"], cwd=new_cookie
    )

    # Install rendered project
    subprocess.check_call(["poetry", "sync"], cwd=new_cookie)
    # Run rendered project's tests
    subprocess.check_call(["poetry", "run", "poe", "test"], cwd=new_cookie)
    # Build container for rendered project
    subprocess.check_call(
        ["docker", "build", ".", "--no-cache"], cwd=new_cookie
    )
