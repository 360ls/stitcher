PACKAGE_DIR=stitcher
DOC_DIR=docs
all: run

install:
	pip install -r requirements.txt

configure:
	python -m $(PACKAGE_DIR).configure

run:
	python -m $(PACKAGE_DIR).run

client:
	python -m $(PACKAGE_DIR).client &

html:
	$(MAKE) -C $(DOC_DIR) html

lint:
	pylint stitcher --rcfile=config/pylintrc

test: lint
	echo "Running tests"

clean:
	find . -name '*.pyc' -delete
