# run for all python files

lint:
	flake8 ./**/*.py
	isort --check --diff ./**/*.py
	black --check ./**/*.py
#	mypy ./**/*.py

format:
	isort ./**/*.py
	black ./**/*.py