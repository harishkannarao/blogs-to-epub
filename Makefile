.DEFAULT_GOAL := run_all

init:
	pip install pipenv --upgrade
	pipenv install --dev

flake8:
	pipenv run flake8 --ignore=E501 --exclude=.venv,.git # ignore max line length

run_all:
	make init flake8

requirements:
	pipenv lock -r > requirements.txt
