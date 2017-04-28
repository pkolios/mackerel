.PHONY: test typing

test: typing
	py.test -v

typing:
	MYPYPATH='' mypy mackerel --ignore-missing-imports
