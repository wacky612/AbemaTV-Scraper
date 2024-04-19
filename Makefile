.PHONY: prepare

prepare: .venv gh-pages

.venv:
	/usr/bin/python -m venv .venv
	$(PWD)/.venv/bin/pip install selenium

gh-pages:
	git clone -b gh-pages git@github.com:wacky612/AbemaTV-Scraper.git gh-pages
