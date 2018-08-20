"""The BaseAPIMethod class."""

from ..session import WowcherAPISession


class BaseAPIMethod:
    """Base class for API methods."""

    def __new__(self, *args, **kwargs):
        """Create API request."""
        data = self.get_data(self, *args, **kwargs)
        response = self.make_request(self, data)
        return self.process_response(self, response)

    def make_request(self, data):
        """Make an API request."""
        return WowcherAPISession.make_request(self, data)
