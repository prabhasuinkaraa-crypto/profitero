SHELL := /bin/bash
PYTHON ?= python3
BEHAVE ?= $(PYTHON) -m behave

.PHONY: help install test test-ui test-api test-scrape clean

help:
	@echo "Targets: install, test, test-ui, test-api, test-scrape, clean"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(BEHAVE)

test-ui:
	$(BEHAVE) -t @ui

test-api:
	$(BEHAVE) -t @api

test-scrape:
	$(BEHAVE) -t @scrape

clean:
	rm -rf .pytest_cache .cache __pycache__ **/__pycache__ artifacts
