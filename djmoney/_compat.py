# flake8: noqa
"""
This module isolates code that has to do with compatibility issues between
different supported versions of Python or other dependencies.

This is quite important to keep the codebase clean.

Please do not catch ImportError exceptions other places than here :)
"""


def setup_managers(sender):
    pass
