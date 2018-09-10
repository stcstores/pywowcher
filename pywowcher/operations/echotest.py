"""The echo_test method of pywowcher."""

from pywowcher import api_methods


def echo_test(message):
    """
    Make an echo test to the Wowcher servers.

    Sends a request containg JSON data to Wowcher, the response to which should
    contain the same JSON data.

    Args:
        message (dict or list): Data to be sent as JSON to Wowcher.
    """
    request = api_methods.EchoTest(message)
    response = request.call()
    return response
