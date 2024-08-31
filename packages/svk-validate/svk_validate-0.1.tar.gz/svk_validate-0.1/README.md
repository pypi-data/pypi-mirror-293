# svk-validate

[![PyPI](https://img.shields.io/pypi/v/svk-validate.svg)](https://pypi.org/project/svk-validate/)
[![Changelog](https://img.shields.io/github/v/release/svkau/svk-validate?include_prereleases&label=changelog)](https://github.com/svkau/svk-validate/releases)
[![Tests](https://github.com/svkau/svk-validate/actions/workflows/test.yml/badge.svg)](https://github.com/svkau/svk-validate/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/svkau/svk-validate/blob/master/LICENSE)


NB! This is a test release. It should work to validate singel XML-files. But don't use this unless you have to :)

A simple tool for validating XML-files against Church of Sweden's adaptation of ERMS.

## Installation

Install this tool using `pip`:
```bash
pip install svk-validate
```
## Usage

For help, run:
```bash
svk-validate --help
```
You can also use:
```bash
python -m svk_validate --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd svk-validate
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
