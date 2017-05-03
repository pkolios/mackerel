.PHONY: lint test typing

lint:
	flake8 --exit-zero mackerel

test: lint typing
	py.test -v

typing:
	MYPYPATH='' mypy mackerel \
			 --disallow-untyped-defs \
			 --ignore-missing-imports \
			 --disallow-untyped-calls
