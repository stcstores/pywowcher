"""The BaseAPIMethod class."""

import logging

import requests

from ..session import WowcherAPISession

logger = logging.getLogger(__name__)


class BaseAPIMethod:
    """Base class for API methods."""

    def __new__(self, *args, **kwargs):
        """Create API request."""
        self.data = self.get_data(self, *args, **kwargs)
        self.response = self.make_request(self)
        return self.process_response(self, self.response)

    def make_request(self):
        """Make an API request."""
        WowcherAPISession.get_credentials()
        headers = WowcherAPISession.get_auth_headers()
        url = f"{WowcherAPISession.DOMAIN}{self.uri}"
        logger.info(f"Making request to {url}")
        logger.debug(f"Sending request data {self.data} to {url}")
        response = requests.post(url, data=self.data, headers=headers)
        logger.debug(f"Recieved response from {url}: {response.text}")
        return response
