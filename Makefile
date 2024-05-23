venv = venv
bin = ${venv}/bin/
pysources = drf_simple_apikey/ example/ tests/

build:
	${bin}python -m build

check:
	${bin}black --check --diff ${pysources}
	make migrations-check

install: install-python

venv:
	python3 -m venv ${venv}

install-python: venv
	${bin}pip install --upgrade pip
	${bin}pip install -e ".[test]"

format:
	${bin}black ${pysources}

migrations:
	@echo "Running migrations..."
	${bin}python -m scripts.makemigrations


migrations-check:
	@echo "Running migrations checks..."
	${bin}python -m scripts.makemigrations --check

test:
	${bin}pytest && TEST_WITH_ROTATION=1 ${bin}pytest