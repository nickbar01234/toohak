VENV=.venv
PYTHON=$(VENV)/bin/python

.PHONY: clean install activate

install: requirements.txt
	python3 -m venv $(VENV);
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf .venv