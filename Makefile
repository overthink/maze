# run `make init`, then use the other targets
# didn't want to depend on init since it takes a while

.PHONY: run
run:
	venv/bin/python maze.py

.PHONY: lint
lint:
	venv/bin/black maze.py

.PHONY: typecheck
typecheck:
	venv/bin/mypy maze.py

.PHONY: test
test: lint typecheck
	venv/bin/python -m unittest *py

.PHONY: init
init: virtualenv

.PHONY: virtualenv
virtualenv: venv/bin/activate
	venv/bin/pip install -U pip
	venv/bin/pip install mypy black

venv/bin/activate:
	which virtualenv || pip install virtualenv
	python -m virtualenv venv
	echo '*' > venv/.gitignore

.PHONY: clean
clean:
	deactivate || true
	rm -rf .mypy_cache __pycache__ venv
