# Executable names
PIP ?= pip
PYTHON ?= python
MKDOCS ?= PYTHONPATH="$(SOURCE_DIR)/tools" mkdocs

# Paths
SOURCE_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT_DIR ?= $(CURDIR)/site

.SUFFIXES:
.PHONY: all install_dependencies docs docs_serve lottie.schema.json validate validate_full


all: docs

lottie.schema.json:$(SOURCE_DIR)/docs/lottie.schema.json

$(SOURCE_DIR)/docs/lottie.schema.json: $(wildcard $(SOURCE_DIR)/schema/**/*.json)
$(SOURCE_DIR)/docs/lottie.schema.json: $(SOURCE_DIR)/tools/schema-merge.py
	$(SOURCE_DIR)/tools/schema-merge.py

docs:$(OUTPUT_DIR)/index.html

$(OUTPUT_DIR)/index.html:$(wildcard $(SOURCE_DIR)/docs/**/*)
$(OUTPUT_DIR)/index.html:$(SOURCE_DIR)/docs/lottie.schema.json
$(OUTPUT_DIR)/index.html:$(SOURCE_DIR)/tools/lottie_markdown.py
	$(MKDOCS) build -f $(SOURCE_DIR)/mkdocs.yml -d $(OUTPUT_DIR)

docs_serve:$(SOURCE_DIR)/docs/lottie.schema.json
	$(MKDOCS) serve -f $(SOURCE_DIR)/mkdocs.yml

install_dependencies:
	$(PIP) install -r $(SOURCE_DIR)/tools/requirements.txt

validate: $(SOURCE_DIR)/docs/lottie.schema.json
	$(SOURCE_DIR)/tools/schema-validate.py


validate_full:$(OUTPUT_DIR)/index.html
	$(SOURCE_DIR)/tools/schema-validate.py --html $(OUTPUT_DIR)/specs
