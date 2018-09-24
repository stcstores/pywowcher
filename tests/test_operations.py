"""Tests for pywowhcer's main methods."""

import pywowcher

from .test_api_methods import mock_echo_test


def test_echo_test_operation(requests_mock):
    """Test the EchoTest operation."""
    message = {"one": "1", "two": "2"}
    mock_echo_test(requests_mock, message)
    assert pywowcher.echo_test(message) == message
