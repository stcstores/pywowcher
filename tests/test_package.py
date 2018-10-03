"""Tests to assert that pywowcher functions correctly as a package."""


import pywowcher


def test_version_info():
    """Check the __version__ file has the neccessary attributes."""
    assert hasattr(pywowcher, "__title__")
    assert hasattr(pywowcher, "__description__")
    assert hasattr(pywowcher, "__url__")
    assert hasattr(pywowcher, "__version__")
    assert hasattr(pywowcher, "__release__")
    assert hasattr(pywowcher, "__author__")
    assert hasattr(pywowcher, "__author_email__")
    assert hasattr(pywowcher, "__license__")
    assert hasattr(pywowcher, "__copyright__")
