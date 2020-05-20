.PHONY: test venv

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
PYTHON_PROJECT_ROOT=.

reset:
	rm -r venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	touch $(VENV_NAME)/bin/activate
	make deps

lint: venv
	${PYTHON} -m pylint **/*.py --rcfile=setup.cfg

deps: venv
	${PYTHON} -m pip install -r ${PYTHON_PROJECT_ROOT}/requirements.txt
	${PYTHON} -m pip install -U pytest pytest-watch python-dotenv pep8 autopep8 pytest-dependency pytest-ordering pylint

update-deps: venv
	pip-compile --no-index --output-file ${PYTHON_PROJECT_ROOT}/requirements.txt ${PYTHON_PROJECT_ROOT}/requirements.in
	make deps

test: venv
	PYTHONPATH=${PYTHON_PROJECT_ROOT} ${PYTHON} -m pytest -vv --disable-pytest-warnings ${ARGS}

test-debug: venv
	PYTHONPATH=${PYTHON_PROJECT_ROOT} ${PYTHON} -m pytest --pdb -vv --disable-pytest-warnings ${ARGS}

test-watch: venv
	PYTHONPATH=${PYTHON_PROJECT_ROOT} $(VENV_NAME)/bin/ptw -- --disable-pytest-warnings ${ARGS}
