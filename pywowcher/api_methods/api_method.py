"""The BaseAPIMethod class."""

import logging

import requests

from ..session import WowcherAPISession

logger = logging.getLogger(__name__)


class BaseAPIMethod:
    """Base class for API methods."""

    POST = "post"
    GET = "get"

    def __new__(self, *args, **kwargs):
        """Create API request."""
        self.data = self.get_data(self, *args, **kwargs)
        self.params = self.get_params(self, *args, **kwargs)
        self.response = self.make_request(self)
        return self.process_response(self, self.response)

    def get_data(self, *args, **kwargs):
        """Return body data for the request."""
        return {}

    def get_params(self, *args, **kwargs):
        """Return URL parameters for the request."""
        return {}

    def process_response(self, response):
        """Process the request response."""
        return response

    def make_request(self):
        """Make an API request."""
        WowcherAPISession.get_credentials()
        headers = WowcherAPISession.get_auth_headers()
        url = f"{WowcherAPISession.DOMAIN}{self.uri}"
        logger.info(f"Making request to {url}")
        logger.debug(f"Sending request data {self.data} to {url}")
        request_kwargs = {
            "url": url,
            "data": self.data,
            "params": self.params,
            "headers": headers,
        }
        if self.method == self.POST:
            response = requests.post(**request_kwargs)
        else:
            response = requests.get(**request_kwargs)
        logger.debug(f"Recieved response from {url}: {response.text}")
        return response
