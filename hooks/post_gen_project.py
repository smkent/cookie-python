import subprocess

# Create empty git repository and add generated files
for call in (
    ["git", "init", "."],
    ["git", "add", "."],
    [
        "git",
        "commit",
        "--author",
        "{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>",
        "-m",
        "Create {{ cookiecutter.project_name }}",
    ],
):
    subprocess.check_call(call)

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
