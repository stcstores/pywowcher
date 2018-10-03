"""WowcherAPISession class."""

import base64
import logging
import os

import yaml

logger = logging.getLogger(__name__)


class WowcherAPISession:
    """Holds the API credentials and the session object."""

    WOWCHER_CREDENTIALS_FILENAME = "wowcher_credentials.yaml"
    DOMAIN = "http://api.staging.redemption.wowcher.co.uk"
    key = None
    secret_token = None

    def get_auth_headers(self):
        """Return authorisation headers."""
        auth_string = f"{self.key}:{self.secret_token}"
        encoded_auth_string = base64.b64encode(auth_string.encode("utf-8"))
        return {"Authorization": encoded_auth_string}

    def get_wowcher_credentials_file(self, directory=None):
        """Return the path to the wowcher credentials file."""
        if directory is None:
            directory = os.getcwd()
        if os.path.exists(os.path.join(directory, self.WOWCHER_CREDENTIALS_FILENAME)):
            return os.path.join(directory, self.WOWCHER_CREDENTIALS_FILENAME)
        elif os.path.dirname(directory) == directory:
            return None
        else:
            return self.get_wowcher_credentials_file(
                directory=os.path.dirname(directory)
            )

    def get_credentials(self):
        """Find API credentials file and load credentials from it."""
        if self.key is not None and self.secret_token is not None:
            return
        credentials_path = self.get_wowcher_credentials_file()
        if credentials_path is None:
            logging.error("Wowcher credentials file not found.")
            raise FileNotFoundError(
                f"{self.WOWCHER_CREDENTIALS_FILENAME} was not found."
            )
        else:
            logger.debug(f"Credentials file found at {credentials_path}")
            self.load_credentials_from_file(credentials_path)

    def load_credentials_from_file(self, credentials_path):
        """Add API credentials from file."""
        logger.info(f"Loading API Credentials from {credentials_path}")
        with open(credentials_path, "r") as config_file:
            config = yaml.load(config_file)
        try:
            self.set_credentials(**config)
        except Exception as e:
            logger.error(f"Could not load config from {credentials_path}.")
            raise e

    def set_credentials(self, key=None, secret_token=None):
        """Set the domain, username and password."""
        if key is not None:
            self.key = key
        if secret_token is not None:
            self.secret_token = secret_token

    def create_credentials_file(self, *, key, secret_token):
        """Create an API credential file."""
        path = os.path.join(os.getcwd(), self.WOWCHER_CREDENTIALS_FILENAME)
        with open(path, "w") as outfile:
            yaml.dump(
                {"key": key, "secret_token": secret_token},
                outfile,
                default_flow_style=False,
            )

    def clear(self):
        """Clear the session credentials."""
        self.key = None
        self.secret_token = None


session = WowcherAPISession()
