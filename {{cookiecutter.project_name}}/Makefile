PIPENV=./pipenv
VENV=.venv
PYTHON_VERSION=$(shell python --version 2>&1 | grep -oe '[0-9]\+\.[0-9]\+')

.PHONY: install
install:
	$(PIPENV) install --python $(PYTHON_VERSION)
	$(VENV)/bin/python setup.py develop --script-dir=bin/

.PHONY: test
test:
	$(PIPENV) install --dev
	$(VENV)/bin/pytest
	$(VENV)/bin/flake8 --exclude='./.*' -- .
