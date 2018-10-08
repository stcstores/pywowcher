"""Base test classes for testing pywowhcer."""

import json
import os
import tempfile

import pytest

import pywowcher


class BasePywowcherTest:
    """Base class for pywowcher tests."""

    fake_live_key = "0ff52fd6-7860-4f07-bab5-5fa74d3b98f0"
    fake_live_secret_token = "16459c82-065a-4e51-b682-c784e404831d"
    fake_staging_key = "a5635153-cf96-4ecf-87b6-b80f0fa1a5ea"
    fake_staging_secret_token = "220d4eb6-3c94-4f0c-b5e8-1befa1a8713c"
    use_staging = True

    @classmethod
    def setup_class(cls):
        """Use a temproary directory as the working directory."""
        pywowcher.session.clear()
        cls.original_working_dir = os.getcwd()
        os.chdir(tempfile.mkdtemp())

    @classmethod
    def teardown_class(cls):
        """Reset the working directory."""
        os.chdir(cls.original_working_dir)

    def setup_method(self):
        """Add a config file to the working directory."""
        pywowcher.session.clear()
        self.create_config_file()

    def teardown_method(self):
        """Reset session class attributes."""
        pywowcher.session.clear()
        if os.path.exists(pywowcher.session.WOWCHER_CREDENTIALS_FILENAME):
            os.remove(pywowcher.session.WOWCHER_CREDENTIALS_FILENAME)

    def create_config_file(self):
        """Add a config file to the working directory."""
        pywowcher.session.create_credentials_file(
            live_key=self.fake_live_key,
            live_secret_token=self.fake_live_secret_token,
            staging_key=self.fake_staging_key,
            staging_secret_token=self.fake_staging_secret_token,
            use_staging=self.use_staging,
        )
        pywowcher.session.clear()
        pywowcher.session.get_credentials()

    @pytest.fixture
    def mock_echo_test(self, requests_mock, echo_test_response):
        """Set up a mocked echo test request."""

        def func(message=None, response=None):
            if message is not None:
                response = {"json": echo_test_response(message)}
            elif response is None:
                raise Exception("Either kwargs or message must be passed")
            if isinstance(response, dict):
                response = [response]
            requests_mock.post(pywowcher.api_methods.EchoTest.get_URL(), response)

        return func

    @pytest.fixture
    def echo_test_response(self):
        """Return the response from the Echo Test API method for a given message."""

        def func(message):
            return {"message": "Echo Test Received", "data": message}

        return func

    @pytest.fixture
    def orders_method_response(self):
        """Return an example response for the Orders API method."""
        with open(
            os.path.join(os.path.dirname(__file__), "order_response.json"), "r"
        ) as f:
            return json.load(f)

    @pytest.fixture
    def mock_orders(self, requests_mock, orders_method_response):
        """Set up a mocked orders request."""

        def func(response_data=None, response=None):
            if response is None and response_data is None:
                response = {"json": orders_method_response}
            elif response_data is not None:
                response = {"json": response_data}
            if isinstance(response, dict):
                response = [response]
            requests_mock.get(pywowcher.api_methods.Orders.get_URL(), response)

        return func

    @pytest.fixture
    def mock_status(self, requests_mock):
        """Set up a mocked status request."""

        def func():
            requests_mock.put(
                pywowcher.api_methods.Status.get_URL(),
                json={"message": "Order status updated", "data": []},
            )

        return func
