"""The Echo Test API Method."""


from .api_method import BaseAPIMethod


class EchoTest(BaseAPIMethod):
    """The Echo Test API method."""

    uri = "/v1/echo"

    def get_data(self, data):
        """Make an Echo test with data."""
        return data

    def process_response(self, response):
        """Process echo response."""
        return response.json()["data"]
