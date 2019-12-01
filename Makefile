.PHONY: default, lint

default:
	python -m houndsploit
lint:
	pylint houndsploit
pep8:
	autopep8 houndsploit --in-place --recursive --aggressive --aggressive
