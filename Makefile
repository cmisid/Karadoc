# OpenBikes API Makefile

## Configuration

PACKAGE    := "karadoc"
BUILD_TIME := $(shell date +%FT%T%z)
PROJECT    := $(shell basename $(PWD))

## Commands

.PHONY: all
all: install 

# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Install dev-dependencies
.PHONY: install-dev
install-dev:
	pip install -r dev-requirements.txt

# Launch test suite
.PHONY: test
test:
	pytest --verbose tests/
