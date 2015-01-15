virtualenv:
	virtualenv .venv
	.venv/bin/pip install -q -r requirements.txt
	.venv/bin/python setup.py develop

lint:
	@find $(sources) -type f\( -iname '*.py' !-iwholename './venv/*' ! -iwholename './tests/*' ! -iwholename './build/*'\) -print0 | xargs -r0 venv/bin/flake8

coverage:
	@venv/bin/nosetests tests --with-coverage --cover-package=gitvendor

test: venv
	@./venv/bin/nosetests tests

clean-all: clean
	rm -rf .venv

clean:
	find . -name \*.pyc -delete
	find . -name '*.bak' -delete
	rm -f .coverage

.PHONY: test clean clean_all lint
