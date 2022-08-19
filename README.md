# [Cookiecutter][cookiecutter] template for new Python projects

[![Build](https://img.shields.io/github/checks-status/smkent/cookie-python/main?label=build)][gh-actions]
[![GitHub stars](https://img.shields.io/github/stars/smkent/cookie-python?style=social)][repo]

[![cookie-python][logo]](#)

A template for new Python projects, with:

* poetry
* pytest
* mypy
* black
* flake8
* GitHub Actions support
* Coverage reports with codecov.io

## Usage

Create a new project from template:

```
pip install cookiecutter
cookiecutter https://github.com/smkent/cookie-python
```

## Development

Prerequisites: [Poetry][poetry]

* Setup: `poetry install`
* Test template rendering and run rendered project tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`
* Update test expected output files from test results:
  `poetry run poe updatetests`

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/smkent/cookie-python/actions?query=branch%3Amain
[logo]: https://raw.github.com/smkent/cookie-python/main/img/cookie-python.png
[poetry]: https://python-poetry.org/docs/#installation
[repo]: https://github.com/smkent/cookie-python
