.PHONY: prepare

prepare: .venv

.venv:
	/usr/bin/python -m venv .venv
	$(PWD)/.venv/bin/pip install selenium
