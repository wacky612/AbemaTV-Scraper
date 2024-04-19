.PHONY: all prepare build deploy

all: prepare build deploy

prepare: .venv gh-pages

.venv:
	/usr/bin/python -m venv .venv
	$(PWD)/.venv/bin/pip install selenium

gh-pages:
	git clone -b gh-pages git@github.com:wacky612/AbemaTV-Scraper.git gh-pages

build:
	$(PWD)/.venv/bin/python main.py > gh-pages/timetable.json

deploy:
	/bin/sh deploy.sh
