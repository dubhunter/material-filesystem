.PHONY: run clean

VENV = venv
PYTHON = $(VENV)/bin/python3
COVERAGE = $(VENV)/bin/coverage
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) app.py

test: $(VENV)/bin/activate
	$(PYTHON) -m unittest discover -s tests

coverage: $(VENV)/bin/activate
	$(COVERAGE) run -m unittest discover -s tests
	$(COVERAGE) report

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf .coverage
	rm -rf $(VENV)
