# OpenBikes API Makefile

## Configuration

PACKAGE    := "karadoc"
BUILD_TIME := $(shell date +%FT%T%z)
PROJECT    := $(shell basename $(PWD))

## Commands

.PHONY: all
all: install 


.PHONY: install
install: ## install dependencies
	pip install -r requirements.txt

.PHONY: love
love:
	@echo "not war !"

.PHONY: help
help: ## print this message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)''


.PHONY: install-dev
install-dev: ## install dev-dependencies
	pip install -r dev-requirements.txt

.PHONY: test 
test: ## launch test suite
	pytest --verbose tests/

.PHONY: tasks
tasks: ## grep TODO and FIXME project-wide
	@grep --exclude-dir=.git --exclude-dir=data --exclude-dir=.idea --exclude=Makefile --exclude=README.md -rEI "TODO|FIXME" .

.PHONY: notebooks
notebooks: ## launch jupyter notebooks
	jupyter notebook notebooks/