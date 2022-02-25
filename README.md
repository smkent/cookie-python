# [Cookiecutter][cookiecutter] template for new Python projects

A template for new Python projects, with:

* pipenv
* pytest
* mypy
* black
* flake8
* GitHub Actions support

## Usage

Create a new project from template:

```
pip install cookiecutter
cookiecutter https://github.com/smkent/cookie-python
```

## Development

* Setup: `make`
* Test template rendering and run rendered project tests: `make test`
* Update or install new dependencies: `make update`
* Fix linting errors: `make lint`

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
