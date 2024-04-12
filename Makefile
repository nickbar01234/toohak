VENV=.venv
PYTHON=$(VENV)/bin/python3.12
SRC=src

.PHONY: clean install test

install: requirements.txt
	python3 -m venv $(VENV);
	$(PYTHON) -m pip install -r requirements.txt

client: install
	.venv/bin/python3.12 src/client.py

server: install
	.venv/bin/python3.12 src/server.py

test:
	cd $(SRC) && python3 -m unittest		

clean:
	rm -rf .venv
