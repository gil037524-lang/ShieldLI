## About The Project
File CLI Tool build 

A simple lightweight, cross-platform file manipulation CLI built with Python using python and stdlibraries. Built as a learning opportunity

### Built With 
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)


## Prerequisites

- Python 3.9 or higher

On newer Linux distros like Ubuntu 23.04+, system Python is protected. You'll need either pipx or a virtual environment to install Python packages.

Installing pipx:

```bash
sudo apt install pipx  # Ubuntu/Deb
```

## Install
1. Clone the repo
```sh
git clone https://github.com/gil037524-lang/ShieldLI.git
```

2. With [pipx](https://pipx.pypa.io/) (recommended):

```bash
pipx install shieldli-0.21-py3-none-any.whl
```

Or with pip:
```bash
pip install shieldli-0.21-py3-none-any.whl
```

Or from the source tarball in a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install shieldli-0.2.tar.gz
```

## Getting Started

1. Install the package using one of the methods above.

2. Verify the install worked:
   ```bash
   filecli help
   ```

3. Try creating and listing a file:
   ```bash
   filecli create myfile.txt "hello world"
   filecli ls
   ```

4. You're ready to go. Use -h or -help to display usage
    ```bash
   filecli -h
   ```
## Usage

```
filecli <command> [args...]

commands:
  list, ls [path]              list files in a directory (default: current dir)
  copy, cp <src> <dst>         copy a file, preserving metadata
  delete, rm, del <path>       delete a file
  merge, cat <a> <b> <out>     concatenate two files into one
  create, cr, touch <path> [content]   create a new file
  help, -h, --help             show help
```
## Development and Testing

```bash
source .venv/bin/activate       
pip install -e ".[dev]"
```

Run tests:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=filecli --cov-report=term-missing -v
```

Lint and format:

```bash
ruff check . --fix
ruff format .
```

## Build
to build your own distributable packages, make edits and run:
```bash
pip install build
python -m build
```
which builds the packages

```
dist/filecli-0.1.0.tar.gz and dist/filecli-0.1.0-py3-none-any.whl
```
## Roadmap

- [ ] Add recursive deletion
- [ ] Add other cool stuff...


## Contributing


### Top contributors:
    Me



## License
Distributed under the Unlicense License. See `LICENSE.txt` for more information.
