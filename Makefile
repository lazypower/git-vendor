.PHONY: clean-all lint test

virtualenv:
	@virtualenv .venv
	@.venv/bin/pip install -q -r requirements.txt
	@.venv/bin/python setup.py develop

lint:
	@find $(sources) -type f \( -iname '*.py' ! -iwholename './.venv/*' ! -iwholename './tests/*'  ! -iwholename './build/*' \) -print0 | xargs -r0 .venv/bin/flake8

test:
	@.venv/bin/py.test

clean-all: clean
	rm -rf .venv

auto:
	@watchmedo shell-command  --patterns="*.py" --ignore-directories --recursive --command "py.test"

clean:
	find . -name \*.pyc -delete
	find . -name '*.bak' -delete
	rm -f .coverage

