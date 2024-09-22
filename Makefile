clean:
	rm -rf dist
	rm -rf py8tb.egg-info
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

dist:
	python setup.py sdist

test:
	pytest py8tb