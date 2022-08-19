# {{ cookiecutter.project_name }}: {{ cookiecutter.project_description }}
{% if cookiecutter.enable_pypi_publish == "yes" %}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_name }})][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_name }})][pypi]{% endif %}{% if cookiecutter.github_user %}
[![Build](https://img.shields.io/github/checks-status/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/main?label=build)][gh-actions]{% if cookiecutter.enable_coverage == "yes" %}
[![codecov](https://codecov.io/gh/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/branch/main/graph/badge.svg)][codecov]{% endif %}
[![GitHub stars](https://img.shields.io/github/stars/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}?style=social)][repo]
{% endif %}{% if cookiecutter.enable_pypi_publish == "yes" and not cookiecutter.github_user %}
{% endif %}
## Development

Prerequisites: [Poetry][poetry]

* Setup: `poetry install`
* Run all tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]
{% if cookiecutter.github_user and cookiecutter.enable_coverage == "yes" %}
[codecov]: https://codecov.io/gh/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}{% endif %}
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
{%- if cookiecutter.github_user %}
[gh-actions]: https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}/actions?query=branch%3Amain{% endif %}
[poetry]: https://python-poetry.org/docs/#installation
{%- if cookiecutter.enable_pypi_publish == "yes" %}
[pypi]: https://pypi.org/project/{{ cookiecutter.project_name }}/{% endif %}
{%- if cookiecutter.github_user %}
[repo]: https://github.com/{{ cookiecutter.github_user }}/{{ cookiecutter.project_name }}{% endif %}
