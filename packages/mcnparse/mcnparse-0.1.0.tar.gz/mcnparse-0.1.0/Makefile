PACKAGE_NAME = mcnparse
VERSION = 0.1.0
PYTHON = .venv/bin/python3

SRC_DIR = $(PACKAGE_NAME)
OUT_DIR = dist
OUT_WHL = $(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl
RELEASE_DIR = release
DOCS_DIR = docs/api

PYTHON_VERSION = ">= 3.11"
define PROJECT_DEPENS
    "numpy==2.1.0",
    "pandas==2.2.2",
    "matplotlib==3.9.2",
    "scipy==1.14.0"
endef

PYPROJECT_TOML_NAME = pyproject.toml
define PYPROJECT_TOML
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "$(PACKAGE_NAME)"
version = "$(VERSION)"
description = "Your package description"
readme = "README.md"
authors = [{name = "Noah J. Blair", email = "noah.blair@colostate.edu"}]
dependencies = [
$(PROJECT_DEPENS)
]
requires-python = $(PYTHON_VERSION)

[tool.hatch.build.targets.wheel]
include = ["$(PACKAGE_NAME)", "tests/**/*", "pyproject.toml", "README.md", "LICENSE"]

[tool.hatch.envs.default]
dependencies = [
    "pylint",
    "ruff",
    "mypy",
    "pytest"
]

endef
export PYPROJECT_TOML

DOXYFILE_NAME = Doxyfile
define DOXYFILE

endef
export DOXYFILE

.PHONY: build docs install clean release test lint

build:
	echo "$$PYPROJECT_TOML" > $(PYPROJECT_TOML_NAME)
	$(PYTHON) -m build
	rm $(PYPROJECT_TOML_NAME)

docs:
	echo "$$DOXYFILE" > $(DOXYFILE_NAME)
	doxygen $(DOXYFILE_NAME)
	rm $(DOXYFILE_NAME)

install:
	echo "$$PYPROJECT_TOML" > $(PYPROJECT_TOML_NAME)
	# $(PYTHON) -m pip install .
	$(PYTHON) -m pip install $(OUT_DIR)/$(OUT_WHL)
	rm $(PYPROJECT_TOML_NAME)

clean:
	rm -rf dist
