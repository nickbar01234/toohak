VENV=.venv
PYTHON=$(VENV)/bin/python
SRC=src

.PHONY: clean install test

install: requirements.txt
	python3 -m venv $(VENV);
	$(PYTHON) -m pip install -r requirements.txt

test:
	cd $(SRC) && python3 -m unittest		

clean:
	rm -rf .venv