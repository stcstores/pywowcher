"""Tests for the session class."""


import os

import pytest
import yaml

import pywowcher

from .basetests import BasePywowcherTest


class TestSession(BasePywowcherTest):
    """Tests for pywowcher API sessions."""

    @pytest.fixture
    def no_config_file(self):
        """Remove the wowcher credentials file from the working directory."""
        os.remove(pywowcher.session.WOWCHER_CREDENTIALS_FILENAME)

    def test_session_domain(self):
        """Test that the WowcherAPISession.domain property returns the correct domain."""
        pywowcher.session.set_credentials(use_staging=False)
        assert pywowcher.session.domain == pywowcher.session.LIVE_DOMAIN
        pywowcher.session.clear()
        pywowcher.session.set_credentials(use_staging=True)
        assert pywowcher.session.domain == pywowcher.session.STAGING_DOMAIN

    def test_clear_session(self):
        """Test that session.clear clears the session."""
        pywowcher.session.get_credentials()
        assert pywowcher.session.live_key is not None
        assert pywowcher.session.live_secret_token is not None
        assert pywowcher.session.staging_key is not None
        assert pywowcher.session.live_secret_token is not None
        assert pywowcher.session.use_staging is not None
        pywowcher.session.clear()
        assert pywowcher.session.live_key is None
        assert pywowcher.session.live_secret_token is None
        assert pywowcher.session.staging_key is None
        assert pywowcher.session.live_secret_token is None
        assert pywowcher.session.use_staging is None

    def test_get_credentials_fails_when_no_file_is_present(self, no_config_file):
        """Test that getting credentials throws and error when no credentials file exists."""
        pywowcher.session.clear()
        with pytest.raises(FileNotFoundError):
            pywowcher.session.get_credentials()

    def test_exception_is_raised_when_config_file_is_malformed(self, no_config_file):
        """Test that an exception is raised when the config file is malformed."""
        pywowcher.session.clear()
        filename = pywowcher.session.WOWCHER_CREDENTIALS_FILENAME
        with open(filename, "w") as f:
            f.write("some text")
        with pytest.raises(Exception):
            pywowcher.session.get_credentials()
        os.remove(filename)

    def test_create_credentials_file(self):
        """Test that the session class can create a credentials file."""
        pywowcher.session.create_credentials_file(
            live_key=self.fake_live_key,
            live_secret_token=self.fake_live_secret_token,
            staging_key=self.fake_staging_key,
            staging_secret_token=self.fake_staging_secret_token,
            use_staging=self.use_staging,
        )
        filename = pywowcher.session.WOWCHER_CREDENTIALS_FILENAME
        assert os.path.exists(filename)
        with open(filename, "r") as config_file:
            config = yaml.load(config_file)
        assert config == {
            "live": {
                "key": self.fake_live_key,
                "secret_token": self.fake_live_secret_token,
            },
            "staging": {
                "key": self.fake_staging_key,
                "secret_token": self.fake_staging_secret_token,
            },
            "use_staging": self.use_staging,
        }
        os.remove(filename)

    def test_can_find_credentials_file(self):
        """Test that Pywowcher can find the credentials file."""
        found_path = pywowcher.session.get_wowcher_credentials_file()
        expected_path = os.path.join(
            os.getcwd(), pywowcher.session.WOWCHER_CREDENTIALS_FILENAME
        )
        assert found_path == expected_path

    def test_session_can_load_credentials(self):
        """Test that session can load credentials from a file."""
        pywowcher.session.clear()
        pywowcher.session.get_credentials()
        assert pywowcher.session.live_key == self.fake_live_key
        assert pywowcher.session.live_secret_token == self.fake_live_secret_token
        assert pywowcher.session.staging_key == self.fake_staging_key
        assert pywowcher.session.staging_secret_token == self.fake_staging_secret_token
        assert pywowcher.session.use_staging == self.use_staging

    def test_session_adds_credentials_when_initialised(self):
        """Test that WowcherAPISession loads credentials on initialisation."""
        session = pywowcher.wowcher_session.WowcherAPISession()
        assert session.live_key == self.fake_live_key
        assert session.live_secret_token == self.fake_live_secret_token
        assert session.staging_key == self.fake_staging_key
        assert session.staging_secret_token == self.fake_staging_secret_token
        assert session.use_staging == self.use_staging

    def test_can_set_session_credentials_manually(self):
        """Test that session credentials can be set manually."""
        live_key = "TEST LIVE KEY"
        live_secret_token = "TEST LIVE TOKEN"
        staging_key = "TEST STAGING KEY"
        staging_secret_token = "TEST STAGING TOKEN"
        use_staging = True
        pywowcher.session.set_credentials(
            live_key=live_key,
            live_secret_token=live_secret_token,
            staging_key=staging_key,
            staging_secret_token=staging_secret_token,
            use_staging=use_staging,
        )
        assert pywowcher.session.live_key == live_key
        assert pywowcher.session.live_secret_token == live_secret_token
        assert pywowcher.session.staging_key == staging_key
        assert pywowcher.session.staging_secret_token == staging_secret_token
        assert pywowcher.session.use_staging == use_staging

    def test_manually_set_credentials_are_not_overwritten(self):
        """Test that session.get_credentials() does not overwrite existing credentials."""
        live_key = "TEST LIVE KEY"
        live_secret_token = "TEST LIVE TOKEN"
        staging_key = "TEST STAGING KEY"
        staging_secret_token = "TEST STAGING TOKEN"
        use_staging = True
        pywowcher.session.set_credentials(
            live_key=live_key,
            live_secret_token=live_secret_token,
            staging_key=staging_key,
            staging_secret_token=staging_secret_token,
            use_staging=use_staging,
        )
        pywowcher.session.get_credentials()
        assert pywowcher.session.live_key == live_key
        assert pywowcher.session.live_secret_token == live_secret_token
        assert pywowcher.session.staging_key == staging_key
        assert pywowcher.session.staging_secret_token == staging_secret_token
        assert pywowcher.session.use_staging == use_staging
