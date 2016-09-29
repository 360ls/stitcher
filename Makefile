PACKAGE_DIR=stitcher
DOC_DIR=docs
all: run

install:
	pip install -r requirements.txt

configure:
	python $(PACKAGE_DIR)/configure.py

run:
	python $(PACKAGE_DIR)/run.py

client:
	python $(PACKAGE_DIR)/client.py &

html:
	$(MAKE) -C $(DOC_DIR) html
