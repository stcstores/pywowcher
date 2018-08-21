"""Tests for the WowcherAPISession class."""

import os
import shutil
import tempfile
import unittest

import yaml

import pywowcher
import requests_mock
from pywowcher import WowcherAPISession
from pywowcher.api_methods.api_method import BaseAPIMethod


class PywowcherTestCase(unittest.TestCase):
    """Base class for Pywowcher tests."""

    key = "0ff52fd6-7860-4f07-bab5-5fa74d3b98f0"
    secret_token = "16459c82-065a-4e51-b682-c784e404831d"


class TestCredentialsFileDoesNotExist(PywowcherTestCase):
    """Tests for when no credentials file exists."""

    def setUp(self):
        """Set the working directory to a temporary directory."""
        os.chdir(tempfile.mkdtemp())

    def tearDown(self):
        """Delete the temporary working directory."""
        shutil.rmtree(str(os.path.abspath(os.getcwd())))

    def test_get_credentials_fails_when_no_file_is_present(self):
        """Test that getting credentials throws and error when no credentials file exists."""
        with self.assertRaises(FileNotFoundError):
            WowcherAPISession.get_credentials()

    def test_create_credentials_file(self):
        """Test that the WowcherAPISession class can create a credentials file."""
        WowcherAPISession.create_credentials_file(
            key=self.key, secret_token=self.secret_token
        )
        filename = WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r") as config_file:
            config = yaml.load(config_file)
        self.assertEqual(config, {"key": self.key, "secret_token": self.secret_token})


class TestCredentialsFileExists(PywowcherTestCase):
    """Tests when a credentials file exists."""

    def setUp(self):
        """Set the working directory to a temp dir and create a credentials file."""
        os.chdir(tempfile.mkdtemp())
        WowcherAPISession.create_credentials_file(
            key=self.key, secret_token=self.secret_token
        )

    def tearDown(self):
        """Delete the temporary working directory."""
        WowcherAPISession.key = None
        WowcherAPISession.secret_token = None
        shutil.rmtree(str(os.path.abspath(os.getcwd())))

    def test_can_find_credentials_file(self):
        """Test that Pywowcher can find the credentials file."""
        found_path = WowcherAPISession.get_wowcher_credentials_file()
        expected_path = os.path.join(
            os.getcwd(), WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
        )
        self.assertEqual(found_path, expected_path)

    def test_session_can_load_credentials(self):
        """Test that WowcherAPISession can load credentials from a file."""
        WowcherAPISession.get_credentials()
        self.assertEqual(WowcherAPISession.key, self.key)
        self.assertEqual(WowcherAPISession.secret_token, self.secret_token)


class TestAPIMethod(TestCredentialsFileExists):
    """Test the pywowhcer.api_methods.api_method.BaseAPIMethod class."""

    TEST_URI = "test_uri"

    def get_test_api_method(self, uri, method):
        """Return a new API method."""
        API_method = BaseAPIMethod
        API_method.uri = uri
        API_method.method = method
        return API_method

    @requests_mock.mock()
    def test_post_request(self, m):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.POST)
        m.post(API_method.get_URL(), text=response_text)
        response = API_method()
        self.assertEqual(response.text, response_text)

    def test_method_get_URL(self):
        """Test the get_URL method of BaseAPIMethod."""
        expected_URL = f"{WowcherAPISession.DOMAIN}{self.TEST_URI}"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.POST)
        self.assertEqual(expected_URL, API_method.get_URL())

    @requests_mock.mock()
    def test_get_request(self, m):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.GET)
        m.get(API_method.get_URL(), text=response_text)
        response = API_method()
        self.assertEqual(response.text, response_text)


class TestEchoTestMethod(TestCredentialsFileExists):
    """Test the EchoTest API method."""

    MESSAGE = {"one": "1", "two": "2"}
    RESPONSE = {"message": "Echo Test Received", "data": MESSAGE}
    API_METHOD = pywowcher.EchoTest

    @requests_mock.mock()
    def test_echo_test_method(self, m):
        """Test the EchoTest API method."""
        m.post(self.API_METHOD.get_URL(), json=self.RESPONSE)
        response = self.API_METHOD(self.MESSAGE)
        self.assertEqual(response, self.MESSAGE)
