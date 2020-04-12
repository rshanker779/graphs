install: clean
	python setup.py sdist bdist_wheel
	pip install dist/*.whl

test:
	black --check .
	pytest --cov 'graphs' --cov-fail-under 90

format:
	black .

doc:
	pip install .[docs]
	sphinx-apidoc -f -o docsrc/source graphs
	make -C docsrc github

clean:
	rm -rf build
	rm -rf dist
	rm -rf graphs.egg-info
	find . -name *.pyc -delete
	find . -name __pycache__ -delete

coverage:
	coverage erase
	pytest --cov 'graphs'
	coverage html

version:
	bump2version --config-file .bumpversion.cfg $(BUMP)

all: install format coverage

