import os
import shutil
import subprocess

TEMPLATE_ONLY_DATA = "cookiecutter_template_data"

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
for call in (
    ["git", "init", "."],
    ["git", "add", "."],
    [
        "git",
        "commit",
        "-m",
        "Create {{ cookiecutter.project_name }}",
    ],
):
    subprocess.run(call, env=environ).check_returncode()

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
