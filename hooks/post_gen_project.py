import itertools
import os
import shutil
import subprocess
from typing import Dict, List

import yaml

TEMPLATE_ONLY_DATA = "cookiecutter_template_data"


def _run(call: List[str], env: Dict[str, str]) -> None:
    subprocess.run(call, env=env).check_returncode()


# Remove files and directories for deselected features
with open(
    os.path.join(os.getcwd(), TEMPLATE_ONLY_DATA, "feature_paths.yml")
) as f:
    feature_paths = yaml.safe_load(f.read())
for rm_path in itertools.chain.from_iterable(
    [
        feature_data["paths"]
        for _, feature_data in feature_paths.items()
        if not feature_data["enabled"]
    ]
):
    full_rm_path = os.path.join(os.getcwd(), rm_path)
    (
        shutil.rmtree(full_rm_path)
        if os.path.isdir(full_rm_path)
        else os.remove(full_rm_path)
    )


# Remove template-only data files
shutil.rmtree(os.path.join(os.getcwd(), TEMPLATE_ONLY_DATA))

# Create empty git repository and add generated files
environ = os.environ.copy()
environ.update(
    dict(
        GIT_AUTHOR_NAME="{{ cookiecutter.author_name }}",
        GIT_AUTHOR_EMAIL="{{ cookiecutter.author_email }}",
        GIT_COMMITTER_NAME="{{ cookiecutter.author_name }}",
        GIT_COMMITTER_EMAIL="{{ cookiecutter.author_email }}",
    )
)

_run(["git", "init", "."], env=environ)

# Set initial branch name to "main"
with open(os.path.join(".git", "HEAD"), "w") as f_ref:
    print("ref: refs/heads/main", file=f_ref)

for call in (
    ["git", "add", "."],
    [
        "git",
        "commit",
        "-m",
        "Create {{ cookiecutter.project_name }}",
    ],
):
    _run(call, env=environ)

print(
    """
{%- if cookiecutter.enable_pypi_publish|lower != 'yes' %}
To enable Coverage reports:
- Set the ENABLE_COVERAGE to true in .github/workflows/ci.yml

{% endif -%}
To enable PyPI publishing:
- (optional) Set the TEST_PYPI_API_TOKEN env var on your GitHub repository
{%- if cookiecutter.enable_pypi_publish|lower != 'yes' %}
- (optional) Set ENABLE_TEST_PYPI_PUBLISH to true in .github/workflows/ci.yml
{%- endif %}
- Set the PYPI_API_TOKEN env var on your GitHub repository
{%- if cookiecutter.enable_pypi_publish|lower != 'yes' %}
- Set ENABLE_PYPI_PUBLISH to true in .github/workflows/ci.yml

{%- endif %}
"""
)
