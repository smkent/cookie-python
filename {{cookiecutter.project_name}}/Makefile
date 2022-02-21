PIPENV=./pipenv
BLACK_ARGS=-l 79
VENV=.venv
SOURCE_DIRS=tests/ {{cookiecutter.project_slug}}/

.PHONY: install
install:
	$(PIPENV) install
	$(VENV)/bin/python setup.py develop --script-dir=bin/

.PHONY: lock
lock:
	$(PIPENV) lock

.PHONY: update
update:
	$(PIPENV) update

.PHONY: testdeps
testdeps:
	$(PIPENV) install --dev

.PHONY: test-full
test-full: testdeps test

.PHONY: test
test:
	$(PIPENV) run flake8 -- .
	$(PIPENV) run isort --quiet --check-only -- $(SOURCE_DIRS)
	$(PIPENV) run black $(BLACK_ARGS) -q --check --diff --color -- $(SOURCE_DIRS)
	$(PIPENV) run mypy
	$(PIPENV) run pytest

.PHONY: lint
lint:
	$(PIPENV) run isort -- $(SOURCE_DIRS)
	$(PIPENV) run black $(BLACK_ARGS) -- $(SOURCE_DIRS)
