# 06.06.2025
Create new rust library by running cmd in main repository folder (Documents/Github):
> cargo new --lib algoxcc

Open as local repository in Github desktop and push to (create in) Github

Open new folder and create this file (PROJECT_LOG.md) and a new README.md file. Commit and push to main.

Copy code from algoxdc to this folder and update Cargo.toml and lib.rs with new name algoxcc

Prepare Python virtual environment and run tests to verify everything is working (both python and rust code)
- Run `cargo test`
- Run `maturin develop -r`

# 30.08.2025
Complete rewrite of rust code including rust and python tests

# 19.09.2025
Create python typing hints

Create a stub file algoxcc.pyi for python type information 
- https://pyo3.rs/v0.26.0/python-typing-hints.html

Syntax of stub file is described here
- https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

# 04.10.2025

Split implementation into two lib packages
- A. with the Rust library for crates.io
- B. jusing A with pyo3/maturin on top for PyPi

Change main structure to a Cargo workspace
- Move current package into a sub folder with same name algoxcc and copy folder into new called algoxcc_py
- Create a new workspace cargo.toml in root algoxcc
- Remove all python/pyo3/maturin from algoxcc
- Remove all logic from algoxcc_py
- Update algoxcc_py to use (deoendency in cargo.toml) algoxcc

Build after changes
> cargo build
> cd algoxcc_py
> maturin develop

# 17.10.2025

Add benchmarks to algoxcc_rust using Criterion
- Add [dev-dependencies] and [[bench]] settings to cargo.toml
- New new folder algoxcc_rust/benches
- New benchmark file xcc_bench.rs in folder
- run cargo bench

Implement benchmark tests for 4 queens problem and 4x4 sudoku

# 21.10.2025

Create an account on crates.io 
- logging in with GitHub account 1Juhler-jdj
- verify email in account settings, and
- create an API token 1Juhler with 365 days validity 
- place it in Dropbox/1Juhler/Udvikling/Rust/crates_io_token.txt
- use it with command cargo login (to save locally)

# 01.11.2025

Build rust documentation using "cargo doc"
- Remove lib algoxcc in algoxcc_python by setting "doc = false"
- Update doc comments

Create a README.md file for the rust library package

Update the cargo.toml file with the mandatory fields: license, authors, description, documentation, repository, keywords and categories

Prepare for publishing using "cargo package"
> cargo package

TODO:



Handle README for each lib (rust and python)

Update workspace README (for github)
- Usage from Rust
- Author
- License

