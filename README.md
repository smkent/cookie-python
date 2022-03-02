# [Cookiecutter][cookiecutter] template for new Python projects

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

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[logo]: https://raw.github.com/smkent/cookie-python/master/img/cookie-python.png
[poetry]: https://python-poetry.org/docs/#installation
