# run for all python files

lint:
	isort --check --diff ./**/*.py
	black --check ./**/*.py
#	mypy ./**/*.py

format:
	isort ./**/*.py
	black ./**/*.py

sam_local:
	sam local start-lambda | sam local start-api