"""WowcherAPISession class."""

import base64
import logging
import os

import requests
import yaml

logger = logging.getLogger(__name__)


class WowcherAPISession:
    """Holds the API credentials and the session object."""

    WOWCHER_CREDENTIALS_FILENAME = "wowcher_credentials.yml"
    DOMAIN = "http://api.staging.redemption.wowcher.co.uk"

    @classmethod
    def make_request(cls, request, data):
        """
        Make an API request.

        Args:
            request: The API Method object. (Instance of BaseAPIMethod).
            data: Dict of data to send with the request. (JSON compatible).
        """
        cls.get_credentials()
        headers = cls.get_auth_headers()
        url = f"{cls.DOMAIN}{request.uri}"
        logger.info(f"Making request to {url}")
        logger.debug(f"Sending request data {data} to {url}")
        response = requests.post(url, data=data, headers=headers)
        logger.debug(f"Recieved response from {url}: {response.text}")
        return response

    @classmethod
    def get_auth_headers(cls):
        """Return authorisation headers."""
        auth_string = f"{cls.key}:{cls.secret_token}"
        encoded_auth_string = base64.b64encode(auth_string.encode("utf-8"))
        return {"Authorization": encoded_auth_string}

    @classmethod
    def get_wowcher_credentials_file(cls, directory=None):
        """Return the path to the wowcher credentials file."""
        if directory is None:
            directory = os.getcwd()
        if os.path.exists(os.path.join(directory, cls.WOWCHER_CREDENTIALS_FILENAME)):
            return os.path.join(directory, cls.WOWCHER_CREDENTIALS_FILENAME)
        elif os.path.dirname(directory) == directory:
            return None
        else:
            return cls.get_wowcher_credentials_file(
                directory=os.path.dirname(directory)
            )

    @classmethod
    def get_credentials(cls):
        """Find API credentials file and load credentials from it."""
        credentials_path = cls.get_wowcher_credentials_file()
        if credentials_path is None:
            logging.error("Wowcher credentials file not found.")
            raise FileNotFoundError(
                f"{cls.WOWCHER_CREDENTIALS_FILENAME} was not found."
            )
        else:
            logger.debug(f"Credentials file found at {credentials_path}")
            cls.load_credentials_from_file(credentials_path)

    @classmethod
    def load_credentials_from_file(cls, credentials_path):
        """Add API credentials from file."""
        logger.info(f"Loading API Credentials from {credentials_path}")
        with open(credentials_path, "r") as config_file:
            config = yaml.load(config_file)
        try:
            cls.add_credentials(**config)
        except Exception as e:
            logger.error(f"Could not load config from {credentials_path}.")
            raise e

    @classmethod
    def add_credentials(cls, key=None, secret_token=None):
        """Set the domain, username and password."""
        if key is not None:
            cls.key = key
        if secret_token is not None:
            cls.secret_token = secret_token

    @classmethod
    def create_credentials_file(cls, *, key, secret_token):
        """Create an API credential file."""
        path = os.path.join(os.getcwd(), cls.WOWCHER_CREDENTIALS_FILENAME)
        with open(path, "w") as outfile:
            yaml.dump(
                {"key": key, "secret_token": secret_token},
                outfile,
                default_flow_style=False,
            )
