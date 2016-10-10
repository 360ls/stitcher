PACKAGE_DIR=stitcher
DOC_DIR=docs
TEST_DIR=test
all: run
TEST_OPTS=--rednose --force-color --verbosity=3

.PHONY: test

install:
	pip install -r requirements.txt

configure:
	python -m $(PACKAGE_DIR).configure

run:
	python -m $(PACKAGE_DIR).app

client:
	python -m $(PACKAGE_DIR).client &

html:
	$(MAKE) -C $(DOC_DIR) html

lint:
	pylint stitcher --rcfile=config/pylintrc

test: lint
	nosetests $(TEST_DIR) $(TEST_OPTS)

clean:
	find . -name '*.pyc' -delete

run-stitcher:
	python -m $(PACKAGE_DIR).app -n --option 3
