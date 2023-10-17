.DEFAULT_GOAL := run_all

init:
	pip install pipenv --upgrade
	pipenv install --dev

unit_test:
	pipenv run python -m pytest tests/unit/ --html=report.html --self-contained-html

test:
	make unit_test

flake8:
	pipenv run flake8 --ignore=E501 --exclude=.venv,.git # ignore max line length

run_all:
	make init test flake8

requirements:
	pipenv lock -r > requirements.txt
