# {{ cookiecutter.project_name }}: {{ cookiecutter.project_description }}
{% if cookiecutter.enable_pypi_publish == "yes" %}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }})][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_name }})][pypi]{% endif %}{% if cookiecutter.github_user %}
[![Build](https://img.shields.io/github/checks-status/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/main?label=build)][gh-actions]{% if cookiecutter.enable_coverage == "yes" %}
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/branch/main/graph/badge.svg)][codecov]{% endif %}
[![GitHub stars](https://img.shields.io/github/stars/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}?style=social)][repo]
{% endif %}{% if (cookiecutter.enable_container_publish == "yes" or cookiecutter.enable_pypi_publish == "yes") and not cookiecutter.github_user %}
{% endif %}{% if cookiecutter.enable_container_publish == "yes" %}
## Installation and usage with Docker

Example `docker-compose.yaml`:

```yaml
version: "3.7"

services:
  {{ cookiecutter.project_name }}:
    image: ghcr.io/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}:latest
    restart: unless-stopped
```

Start the container by running:

```console
docker-compose up -d
```

Debugging information can be viewed in the container log:

```console
docker-compose logs -f
```
{% endif %}{% if cookiecutter.enable_pypi_publish == "yes" %}
## Installation from PyPI

[{{ cookiecutter.project_name }} is available on PyPI][pypi]:

```console
pip install {{ cookiecutter.project_name }}
```
{% endif %}
## Development

### [Poetry][poetry] installation

Via [`pipx`][pipx]:

```console
pip install pipx
pipx install poetry
pipx inject poetry poetry-pre-commit-plugin
```

Via `pip`:

```console
pip install poetry
poetry self add poetry-pre-commit-plugin
```

### Development tasks

* Setup: `poetry install`
* Run static checks: `poetry run poe lint` or
  `poetry run pre-commit run --all-files`
* Run static checks and tests: `poetry run poe test`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]
{% if cookiecutter.github_user and cookiecutter.enable_coverage == "yes" %}
[codecov]: https://codecov.io/gh/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}{% endif %}
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
{%- if cookiecutter.github_user %}
[gh-actions]: https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/actions?query=branch%3Amain{% endif %}
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/docs/#installation
{%- if cookiecutter.enable_pypi_publish == "yes" %}
[pypi]: https://pypi.org/project/{{ cookiecutter.project_name }}/{% endif %}
{%- if cookiecutter.github_user %}
[repo]: https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}{% endif %}
