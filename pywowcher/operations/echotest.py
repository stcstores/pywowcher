"""The echo_test method of pywowcher."""

from pywowcher import api_methods


def echo_test(message):
    """
    Make an echo test to the Wowcher servers.

    Test access to the Wowcher servers by sending JSON serialized data. If the request
    is completed successfully the same data should be returned.

    :param message: Data to be sent as JSON to Wowcher.
    :type message: dict or list

    :rtype: dict or list
    """
    request = api_methods.EchoTest(message)
    response = request.call()
    return response
