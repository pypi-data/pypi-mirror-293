# Dataset library prototype

Sedpack: scalable and efficient data packing

This is a prototype of a dataset library. Mainly refactored from the [SCAAML](https://github.com/google/scaaml) project.

## Available components

- TODO

## Install

### Dependencies

To use this library you need to have a working version of [TensorFlow 2.x](https://www.tensorflow.org/install) and a version of Python >=3.8.

### Dataset install

#### Development install

1. Clone the repository: `git clone https://security-and-privacy-group-research.googlesource.com/dataset_lib_prototype`
2. Install dependencies: `python3 -m pip install --require-hashes -r requirements.txt`
3. Install the package in development mode: `python3 -m pip install --editable .` (short `pip install -e .` or legacy `python setup.py develop`)

### Update dependencies

Make sure to have: `sudo apt install python3 python3-pip python3-venv` and
activated the virtual environment.

Install requirements: `pip install --require-hashes -r base-tooling-requirements.txt`

Update: `pip-compile requirements.in --generate-hashes --upgrade` and commit requirements.txt.

#### Package install

`pip install TODO(package name)`

### Tutorial

TODO provide instructions how to use this package.

## Disclaimer

This is not an official Google product.
