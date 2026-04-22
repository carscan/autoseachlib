"""
AutoSeachLib — Automated Research Library for CarScan.ai
========================================================

A framework for autonomous experimentation and optimization
of damage detection models.

Usage:
    >>> import autoseachlib
    >>> autoseachlib.hello_world()
    Hello World from AutoSeachLib!

    >>> autoseachlib.add_strings("Hello, ", "World!")
    'Hello, World!'
"""

from autoseachlib.core import hello_world, add_strings
from autoseachlib.s3 import download_image

__version__ = "0.1.0"

__all__ = [
    "hello_world",
    "add_strings",
    "download_image",
    "__version__",
]
