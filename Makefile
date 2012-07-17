SHELL := /bin/bash
TESTS=$(shell find tests/ -name "*.py")


check:
	nosetests ${TESTS}
