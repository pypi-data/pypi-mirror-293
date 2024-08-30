"""These tests are meant to check whether certain imports are valid.

This is a way to ensure that the package namespacing doesn't get messed
with and that every important import remains valid.
"""

import importlib

import pytest


@pytest.mark.parametrize("package_name", ["slimify"])
def test_import_package(package_name: str) -> None:
    """Ensures that packages are importable."""
    importlib.import_module(package_name)
