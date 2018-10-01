"""The BaseAPIMethod class."""

import logging

import requests

from ..session import WowcherAPISession

logger = logging.getLogger(__name__)


class BaseAPIMethod:
    """Base class for API methods."""

    POST = "post"
    GET = "get"
    PUT = "put"

    response = None

    data = None
    json = None
    params = None

    request_methods = {POST: requests.post, GET: requests.get, PUT: requests.put}

    def __init__(self, *args, **kwargs):
        """Create API request."""
        self.prepare_data(*args, **kwargs)

    def call(self):
        """Make the API request."""
        self.response = self.make_request()
        return self.process_response(self.response)

    def prepare_data(self, *args, **kwargs):
        """Prepare request data."""
        self.data = self.get_data(*args, **kwargs) or None
        self.json = self.get_json(*args, **kwargs) or None
        self.params = self.get_params(*args, **kwargs) or None

    def get_data(self, *args, **kwargs):
        """Return body data for the request."""
        return {}

    def get_json(self, *args, **kwargs):
        """Return json data for the request."""
        return {}

    def get_params(self, *args, **kwargs):
        """Return URL parameters for the request."""
        return {}

    def process_response(self, response):
        """Process the request response."""
        return response

    @classmethod
    def get_URL(cls):
        """Return the complete URL for the API method."""
        return f"{WowcherAPISession.DOMAIN}{cls.uri}"

    def make_request(self):
        """Make an API request."""
        WowcherAPISession.get_credentials()
        headers = WowcherAPISession.get_auth_headers()
        url = self.get_URL()
        logger.info(f"Making request to {url}")
        logger.debug(f"Sending request data {self.data} to {url}")
        self.response = requests.request(
            method=self.method,
            url=url,
            data=self.data,
            json=self.json,
            params=self.params,
            headers=headers,
        )
        logger.debug(
            (
                f"Recieved response from {url} Status: "
                f"{self.response.status_code} text: {self.response.text}"
            )
        )
        self.response.raise_for_status()
        return self.response
