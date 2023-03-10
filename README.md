# Hide It
[![Python 3.9.7](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/) 

Hide It is an application allowing users to create overlay windows that always stay on top, change their dimensions, color and opacity, save and load overlay presets. 

## Features

Illustration|Feature|
:----------:|:------|
![open_new.gif](https://s9.gifyu.com/images/open_new.gif) | Create new overlay window by clicking on "Open new" button in Overlays Actions frame. Click and drag any overlay corner to resize. Click on overlay center and drag to move it. Change color by entering [3- or 6-digit hex value](https://www.w3schools.com/colors/colors_hexadecimal.asp). Change overlay opacity by entering a float in range between 0 and 1.
![load_save.gif](https://s3.gifyu.com/images/load_save.gif) | Save and load overlay config files by clicking on "Load" and "Save" buttons in Config frame.
![lock_unlock.gif](https://s9.gifyu.com/images/lock_unlock.gif) | Make overlays transparent to mouse clicks and keyboard actions by clicking on "Lock" button in Overlay Actions.
![close_all.gif](https://s9.gifyu.com/images/close_all.gif) | Close all overlays by clicking on "Close all" button in Overlays Actions frame.
![show_hide.gif](https://s9.gifyu.com/images/show_hide.gif) | Toggle overlays visibility with "Hide" and "Show" buttons in Overlays Actions.

## Getting Started
### Hide It standalone executable
* Download latest physical remote [release](https://github.com/k5md/Hide-It/releases/latest)
* Unpack archive to any directory
* Run hide_it binary

## Development
### Environment setup
1.  Install Python 3.9+
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

### Module/gui code running
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

## Contributions
PR are always welcome!