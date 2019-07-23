#!/usr/bin/env bash

set -u

pylint --rcfile=.pylint.cfg $(find tests/ -name "*.py" -print) --output-format=colorized
pylint --rcfile=.pylint.cfg $(find es_downloader/ -name "*.py" -print) --output-format=colorized
