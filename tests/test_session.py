"""Tests for the WowcherAPISession class."""

import os
import shutil
import tempfile
import unittest

import yaml

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

    @requests_mock.mock()
    def test_make_requestMethod(self, m):
        """Test the WowcherAPISession.make_request method."""
        test_uri = "test_uri"

        class TestMethod(BaseAPIMethod):
            uri = test_uri

            def get_data(self):
                return {}

            def process_response(self, response):
                return response

        response_text = "hello"
        m.post(f"{WowcherAPISession.DOMAIN}{test_uri}", text=response_text)
        response = TestMethod()
        self.assertEqual(response.text, response_text)
