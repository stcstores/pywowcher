"""Tests for the WowcherAPISession class."""


import os

import pytest
import pywowcher
import yaml

from .basetests import BasePywowcherTest


class TestSession(BasePywowcherTest):
    """Tests for pywowcher API sessions."""

    @pytest.fixture
    def no_config_file(self):
        """Remove the wowcher credentials file from the working directory."""
        os.remove(pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME)

    def test_get_credentials_fails_when_no_file_is_present(self, no_config_file):
        """Test that getting credentials throws and error when no credentials file exists."""
        with pytest.raises(FileNotFoundError):
            pywowcher.WowcherAPISession.get_credentials()

    def test_exception_is_raised_when_config_file_is_malformed(self, no_config_file):
        """Test that an exception is raised when the config file is malformed."""
        filename = pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
        with open(filename, "w") as f:
            f.write("some text")
        with pytest.raises(Exception):
            pywowcher.WowcherAPISession.get_credentials()
        os.remove(filename)

    def test_create_credentials_file(self):
        """Test that the WowcherAPISession class can create a credentials file."""
        pywowcher.WowcherAPISession.create_credentials_file(
            key=self.fake_key, secret_token=self.fake_secret_token
        )
        filename = pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
        assert os.path.exists(filename)
        with open(filename, "r") as config_file:
            config = yaml.load(config_file)
        assert config == {"key": self.fake_key, "secret_token": self.fake_secret_token}
        os.remove(filename)

    def test_can_find_credentials_file(self):
        """Test that Pywowcher can find the credentials file."""
        found_path = pywowcher.WowcherAPISession.get_wowcher_credentials_file()
        expected_path = os.path.join(
            os.getcwd(), pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
        )
        assert found_path == expected_path

    def test_session_can_load_credentials(self):
        """Test that WowcherAPISession can load credentials from a file."""
        pywowcher.WowcherAPISession.get_credentials()
        assert pywowcher.WowcherAPISession.key == self.fake_key
        assert pywowcher.WowcherAPISession.secret_token == self.fake_secret_token
