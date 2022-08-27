# [Cookiecutter][cookiecutter] template for new Python projects

[![Build](https://img.shields.io/github/checks-status/smkent/cookie-python/main?label=build)][gh-actions]
[![GitHub stars](https://img.shields.io/github/stars/smkent/cookie-python?style=social)][repo]

[![cookie-python][logo]](#)

A template for new Python projects, with:

* [poetry][poetry] (with [poetry-dynamic-versioning][poetry-dynamic-versioning])
* [pytest][pytest]
* [mypy][mypy]
* [black][black]
* [flake8][flake8] (with [bugbear][flake8-bugbear], [simplify][flake8-simplify],
  and [pep8-naming][pep8-naming])
* [bandit][bandit]
* [cruft][cruft]
* GitHub Actions support
* Coverage reports with [codecov.io][codecov]

## New project creation

### With [cruft][cruft] via script

```python
pip install poetry
poetry install
poetry run new-cookie <path>  # or poetry run cruft create
```

### With [cookiecutter][cookiecutter] directly

```python
pip install cookiecutter
cookiecutter https://github.com/smkent/cookie-python
```

## Development

Prerequisites: [Poetry][poetry-installation]

* Setup: `poetry install`
* Test template rendering and run rendered project tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`
* Update test expected output files from test results:
  `poetry run poe updatetests`

[bandit]: https://github.com/PyCQA/bandit
[black]: https://github.com/psf/black
[codecov]: https://codecov.io
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cruft]: https://github.com/cruft/cruft
[flake8]: https://github.com/pycqa/flake8
[flake8-bugbear]: https://github.com/PyCQA/flake8-bugbear
[flake8-simplify]: https://github.com/MartinThoma/flake8-simplify
[gh-actions]: https://github.com/smkent/cookie-python/actions?query=branch%3Amain
[logo]: https://raw.github.com/smkent/cookie-python/main/img/cookie-python.png
[mypy]: https://github.com/python/mypy
[pep8-naming]: https://github.com/PyCQA/pep8-naming
[poetry-dynamic-versioning]: https://github.com/mtkennerly/poetry-dynamic-versioning
[poetry-installation]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org/
[pytest]: https://docs.pytest.org
[repo]: https://github.com/smkent/cookie-python
