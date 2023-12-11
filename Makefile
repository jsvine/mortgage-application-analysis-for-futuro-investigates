.PHONY: README.md venv data analysis

PYTHON_DIRS=scripts notebooks/utils
NOTEBOOKS=notebooks/00-descriptive-statistics.ipynb notebooks/01-regression.ipynb

requirements.txt: requirements.in
	pip-compile requirements.in

venv:
	python -m venv venv
	venv/bin/pip install pip-tools
	venv/bin/pip-sync

format:
	isort $(PYTHON_DIRS) --skip .ipynb_checkpoints
	black $(PYTHON_DIRS) --exclude .ipynb_checkpoints
	nbqa isort $(NOTEBOOKS)
	nbqa black $(NOTEBOOKS)

lint:
	isort --check $(PYTHON_DIRS) --skip .ipynb_checkpoints
	black --check $(PYTHON_DIRS) --exclude .ipynb_checkpoints
	flake8 --max-line-length 88 --extend-ignore E203 $(PYTHON_DIRS) --exclude .ipynb_checkpoints
	nbqa flake8 $(NOTEBOOKS) --max-line-length 88

data:
	python scripts/00-download-data.py
	python scripts/01-generate-data-samples.py
	python scripts/02-filter-mortgages.py
	python scripts/03-process-institutions.py
	python scripts/04-process-census.py

analysis:
	nbexec notebooks
