# Executable names
PIP ?= pip
PYTHON ?= python
MKDOCS ?= mkdocs

# Paths
SOURCE_DIR = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT_DIR ?= $(CURDIR)/site

.SUFFIXES:
.PHONY: all install_dependencies docs docs_serve lottie.schema.json validate validate_full validate_animations


all: docs

lottie.schema.json:$(SOURCE_DIR)/docs/lottie.schema.json

$(SOURCE_DIR)/docs/lottie.schema.json: $(wildcard $(SOURCE_DIR)/schema/**/*.json)
	schema-merge.py

docs:$(OUTPUT_DIR)/index.html

$(OUTPUT_DIR)/index.html:$(wildcard $(SOURCE_DIR)/docs/**/*)
$(OUTPUT_DIR)/index.html:$(SOURCE_DIR)/docs/lottie.schema.json
	$(MKDOCS) build -f $(SOURCE_DIR)/mkdocs.yml -d $(OUTPUT_DIR)

docs_serve:$(SOURCE_DIR)/docs/lottie.schema.json
	$(MKDOCS) serve -f $(SOURCE_DIR)/mkdocs.yml

install_dependencies:
	$(PIP) install -r $(SOURCE_DIR)/tools/requirements.txt

validate: $(SOURCE_DIR)/docs/lottie.schema.json
	schema-validate.py


validate_full:$(OUTPUT_DIR)/index.html
	schema-validate.py --html $(OUTPUT_DIR)/specs

validate_animations: $(SOURCE_DIR)/docs/lottie.schema.json
validate_animations: $(SOURCE_DIR)/tests/validate_animations.test.js
validate_animations: $(wildcard $(SOURCE_DIR)/tests/**/*.json)
validate_animations: $(wildcard $(SOURCE_DIR)/docs/static/examples/**/*.json)
	npm test
