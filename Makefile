curdir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all prepare build deploy

all: prepare build deploy

prepare: .venv gh-pages

.venv:
	/usr/bin/python -m venv .venv
	$(curdir)/.venv/bin/pip install selenium webdriver-manager

gh-pages:
	git clone -b gh-pages git@github.com:wacky612/AbemaTV-Scraper.git gh-pages

build:
	$(curdir)/.venv/bin/python main.py > gh-pages/timetable.json

deploy:
	/bin/sh deploy.sh
