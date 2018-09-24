"""Tests for pywowhcer's main methods."""

import pywowcher

MESSAGE = {"one": "1", "two": "2"}
RESPONSE = {"message": "Echo Test Received", "data": MESSAGE}
API_METHOD = pywowcher.api_methods.EchoTest


def test_echo_test_method(requests_mock):
    """Test the EchoTest API method."""
    requests_mock.post(pywowcher.api_methods.EchoTest.get_URL(), json=RESPONSE)
    assert pywowcher.echo_test(MESSAGE) == MESSAGE
