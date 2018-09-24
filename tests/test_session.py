"""Tests for the WowcherAPISession class."""


import os

import yaml

import pytest
import pywowcher

fake_key = "0ff52fd6-7860-4f07-bab5-5fa74d3b98f0"
fake_secret_token = "16459c82-065a-4e51-b682-c784e404831d"


@pytest.fixture
def temporary_cwd(tmpdir):
    """Use a temporary directory as the working directory."""
    os.chdir(tmpdir.mkdir("temp_working_directory"))

    def create_temporary_working_directory(config_file=True):
        if config_file is True:
            pywowcher.WowcherAPISession.create_credentials_file(
                key=fake_key, secret_token=fake_secret_token
            )
            pywowcher.WowcherAPISession.key = None
            pywowcher.WowcherAPISession.secret_token = None

    return create_temporary_working_directory


def test_get_credentials_fails_when_no_file_is_present(temporary_cwd):
    """Test that getting credentials throws and error when no credentials file exists."""
    temporary_cwd(config_file=False)
    pywowcher.WowcherAPISession.key = None
    pywowcher.WowcherAPISession.secret_token = None
    with pytest.raises(FileNotFoundError):
        pywowcher.WowcherAPISession.get_credentials()


def test_exception_is_raised_when_config_file_is_malformed(temporary_cwd):
    """Test that an exception is raised when the config file is malformed."""
    temporary_cwd(config_file=False)
    with open(pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME, "w") as f:
        f.write("some text")
    with pytest.raises(Exception):
        pywowcher.WowcherAPISession.get_credentials()


def test_create_credentials_file(temporary_cwd):
    """Test that the WowcherAPISession class can create a credentials file."""
    temporary_cwd(config_file=False)
    pywowcher.WowcherAPISession.create_credentials_file(
        key=fake_key, secret_token=fake_secret_token
    )
    filename = pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
    assert os.path.exists(filename)
    with open(filename, "r") as config_file:
        config = yaml.load(config_file)
    assert config == {"key": fake_key, "secret_token": fake_secret_token}


def test_can_find_credentials_file(temporary_cwd):
    """Test that Pywowcher can find the credentials file."""
    temporary_cwd(config_file=True)
    found_path = pywowcher.WowcherAPISession.get_wowcher_credentials_file()
    expected_path = os.path.join(
        os.getcwd(), pywowcher.WowcherAPISession.WOWCHER_CREDENTIALS_FILENAME
    )
    assert found_path == expected_path


def test_session_can_load_credentials(temporary_cwd):
    """Test that WowcherAPISession can load credentials from a file."""
    temporary_cwd(config_file=True)
    pywowcher.WowcherAPISession.get_credentials()
    assert pywowcher.WowcherAPISession.key == fake_key
    assert pywowcher.WowcherAPISession.secret_token == fake_secret_token
