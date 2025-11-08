# Local development

## Python

### Setup

Create a virtual environment for python and instal maturin for building the module and pytest for running python tests

`pip install -r requirements.txt`

### Development and test

For local build and test use `maturin develop` with optional `--release` flag for performance optimization.

Python interface is tested using pytest with tests in folder pytests

### Build

To create a wheel for distribution use `maturin build --release` or `maturin build -r`

### Usage in local python code
Build performance optimized local wheel `maturin build -r`

Copy wheel to sub folder named algoxcc in python project folder