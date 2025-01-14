# test-baked-cookie: This is a test project called "test-baked-cookie"

[![Build](https://img.shields.io/github/checks-status/ness/test-baked-cookie/main?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/ness/test-baked-cookie/branch/main/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/ness/test-baked-cookie?style=social)][repo]

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

[codecov]: https://codecov.io/gh/ness/test-baked-cookie
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/ness/test-baked-cookie/actions?query=branch%3Amain
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/docs/#installation
[repo]: https://github.com/ness/test-baked-cookie
