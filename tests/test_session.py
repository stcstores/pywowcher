"""Tests for the WowcherAPISession class."""


import os
import tempfile

import yaml

from pywowcher import WowcherAPISession

from .pywowcher_test_case import PywowcherTestCase


class TestCredentialsFileDoesNotExist(PywowcherTestCase):
    """Tests for when no credentials file exists."""

    def create_working_directory(self):
        """Set the working directory to a temp dir without a credentials file."""
        os.chdir(tempfile.mkdtemp())

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
