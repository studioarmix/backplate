
.PHONY: clean test build publish

build: clean test
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf ./dist ./build

test:
	flake8

publish:
	twine upload ./dist/*
