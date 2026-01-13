# [Cookiecutter][cookiecutter] template for new Python projects

[![PyPI](https://img.shields.io/pypi/v/cookie-python)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookie-python)][pypi]
[![Build](https://img.shields.io/github/checks-status/smkent/cookie-python/main?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/cookie-python/branch/main/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/cookie-python?style=social)][repo]

[![cookie-python][logo]](#)

A template for new Python projects, with:

* [poetry][poetry] (with [poetry-dynamic-versioning][poetry-dynamic-versioning])
* [pytest][pytest]
* [pre-commit][pre-commit]
* [mypy][mypy]
* [ruff][ruff]
* [bandit][bandit]
* [cruft][cruft]
* GitHub Actions support
* Coverage reports with [codecov.io][codecovio]

## Poetry installation

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

## New project creation

### With [cruft][cruft] via script

```console
poetry install
poetry run new-cookie <path>  # or poetry run cruft create
```

### With [cookiecutter][cookiecutter] directly

```console
pip install cookiecutter
cookiecutter https://github.com/smkent/cookie-python
```

## Development tasks

* Setup: `poetry install`
* Run static checks: `poetry run poe lint` or
  `poetry run pre-commit run --all-files`
* Run static checks and tests: `poetry run poe test`
* Update test expected output files from test results:
  `poetry run poe updatetests`

[bandit]: https://github.com/PyCQA/bandit
[codecov]: https://codecov.io/gh/smkent/cookie-python
[codecovio]: https://codecov.io
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cruft]: https://github.com/cruft/cruft
[gh-actions]: https://github.com/smkent/cookie-python/actions?query=branch%3Amain
[logo]: https://raw.github.com/smkent/cookie-python/main/img/cookie-python.png
[mypy]: https://github.com/python/mypy
[pipx]: https://pypa.github.io/pipx/
[poetry-dynamic-versioning]: https://github.com/mtkennerly/poetry-dynamic-versioning
[poetry-installation]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org/
[pre-commit]: https://pre-commit.com/
[pypi]: https://pypi.org/project/cookie-python/
[pytest]: https://docs.pytest.org
[repo]: https://github.com/smkent/cookie-python
[ruff]: https://github.com/astral-sh/ruff
