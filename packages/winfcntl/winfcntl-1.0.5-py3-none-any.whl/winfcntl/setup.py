from setuptools import setup, find_packages

VERSION = '1.0.5'
DESCRIPTION = 'A fcntl solution for Windows Operating System'
LONG_DESCRIPTION = """
A fcntl solution for Windows Operating System created to handle ModuleNotFoundError issues. This package replicates fcntl functionality for Windows, addressing compatibility issues where Unix-specific modules are required but not available.

### How to Use

This package can be used as a replacement for fcntl in Python modules that need cross-platform file control. Import `winfcntl` when running on Windows and `fcntl` on Unix-based systems.

### Usage for Library Developers

Library developers can check the operating system using `os.name` or `platform.system()` to decide whether to import `winfcntl` (for Windows) or `fcntl` (for Unix-based systems). The function names and interfaces are designed to be compatible with `fcntl`.

### Changelog

### Version 1.0.1
- Fixed a small mistake disabling other programs from using the Fcntl class.

### Version 1.0.0
- Initial release.


### Acknowledgments

Thank you to Kiamehr Eskandari for developing this package.
"""

setup(
    name="winfcntl",
    version=VERSION,
    author="Kiamehr Eskandari",
    author_email="kiamehr13922014@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['fcntl', 'windows', 'module', 'package', 'library'],
    classifiers=[
        "Development Status :: 3 - Alpha", 
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
