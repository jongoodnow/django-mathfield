clean:
	rm -rf build
	rm -rf dist

reinstall:
	pip uninstall -y django-mathfield
	python setup.py install

test:
	python -Wall manage.py test

publish:
	python setup.py sdist upload