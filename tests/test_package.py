"""Tests to assert that pywowcher functions correctly as a package."""


from pywowcher import __version__


def test_version_info():
    """Check the __version__ file has the neccessary attributes."""
    assert hasattr(__version__, "__title__")
    assert hasattr(__version__, "__description__")
    assert hasattr(__version__, "__url__")
    assert hasattr(__version__, "__version__")
    assert hasattr(__version__, "__author__")
    assert hasattr(__version__, "__author_email__")
    assert hasattr(__version__, "__license__")
    assert hasattr(__version__, "__copyright__")
