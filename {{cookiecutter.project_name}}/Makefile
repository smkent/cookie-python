PIPENV=./pipenv
VENV=.venv

.PHONY: install
install:
	$(PIPENV) install
	$(VENV)/bin/python setup.py develop --script-dir=bin/

.PHONY: test
test:
	$(PIPENV) install --dev
	$(VENV)/bin/pytest
	$(VENV)/bin/flake8 --exclude='./.*' -- .
