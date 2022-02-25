PIPENV=./pipenv
BLACK_ARGS=-l 79
SOURCE_DIRS=tests/ hooks/

.PHONY: all
all: rm sync

.PHONY: testall
testall: all test

.PHONY: rm
rm:
	-$(PIPENV) --rm

.PHONY: sync
sync:
	$(PIPENV) sync --dev
	$(PIPENV) run python setup.py develop --script-dir=bin/

.PHONY: update
update:
	$(PIPENV) update --dev
	@# https://github.com/Madoshakalaka/pipenv-setup/issues/101
	SETUPTOOLS_USE_DISTUTILS=stdlib $(PIPENV) run pipenv-setup sync --pipfile
	$(PIPENV) run python setup.py develop --script-dir=bin/

.PHONY: ci
test-ci:
	$(PIPENV) run tox

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

.PHONY: dist
dist:
	$(PIPENV) run python -m build --sdist --wheel --outdir=dist
