# Hide It
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

## Getting Started
### Physical remote GUI standalone executable
* Download latest physical remote [release](https://github.com/k5md/Hide-It/releases/latest)
* Unpack archive to any directory
* Run hide_it binary

## Development
### Environment setup
1.  Install Python 3.7+
2.  Install `virtualenv`
    ```sh
    pip install virtualenv
    ```
3.  Clone this project
4.  From project directory, run
    ```sh
    virtualenv .env
    ```
    **Note**: This will create a virtual environment using the Python version
    that `virtualenv` was run with (which will be the version it was installed
    with). To use a specific Python version, run:
    ```sh
    virtualenv --python=<path_to_other_python_version> .env
    # For example, this might look like
    virtualenv --python=/usr/bin/python3.6 .env
    ```
5.  Assuming you are using the `bash` shell, run:
    ```sh
    source .env/bin/activate
    ```
    For other shells, see the other `activate.*` scripts in the `.env/bin/`
    directory. If you are on Windows, run:
    ```sh
    .env\Scripts\activate.bat
    ```
6.  Install all of the required packages using
    ```sh
    pip install -r requirements.txt
    ```

### Module/cli/gui code running
With virtual environment active, execute one of the following commands from **src** project directory:
```sh
python -m hide_it
```

### Creating portable executables
This project employs pyinstaller to create binaries. To generate executables from sources on your PC:
1. Enter the virtual environment (run `source .env/bin/activate` or OS/shell equivalent).
2.  Run the following command to create bundles with binaries in project's dist directory
    ```sh
    python package.py
    ```
Generated archives will be placed in **artifacts** directory
### Packaging module
Run the following command to package hide_it module:
```sh
python -m pip install --upgrade build
python -m build
```
Generated archive and .whl package will be placed in **dist** directory.

## Contributions
PR are always welcome!

## Todo
- add extension to config file when saved
- separate overlay widget features from non-related stuff
- move ^ to separate module
- move ResizeGrip and related stuff to a Resizable subclass 
- move ^ to a separate module
- change app icon
- add description to readme
- add illustrations to readme