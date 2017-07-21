.PHONY: lint test typing docs release

lint:
	flake8 --exit-zero mackerel

test: lint typing
	py.test -v --cov=mackerel

typing:
	MYPYPATH='' mypy mackerel \
			 --disallow-untyped-defs \
			 --ignore-missing-imports \
			 --disallow-untyped-calls

docs:
	PYTHONPATH=$$PYTHONPATH:$(pwd) python mackerel/cli.py build docs

release:
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
