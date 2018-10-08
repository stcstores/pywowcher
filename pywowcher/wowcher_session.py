"""WowcherAPISession class."""

import base64
import logging
import os

import yaml

logger = logging.getLogger(__name__)


class WowcherAPISession:
    """Holds the API credentials and settings."""

    WOWCHER_CREDENTIALS_FILENAME = "wowcher_credentials.yaml"
    LIVE_DOMAIN = "http://api.redemption.wowcher.co.uk"
    STAGING_DOMAIN = "http://api.staging.redemption.wowcher.co.uk"

    staging_key = None
    staging_secret_token = None

    live_key = None
    live_secret_token = None

    use_staging = None

    def __init__(self, load_credentials=True):
        """
        Set the API credentials and settings.

        :param load_credentials bool: If True an attempt will be made to load credentials
            and settings from `wowcher_credentials.yaml`, if False no attempt will be
            made.
        """
        if load_credentials is True:
            try:
                self.get_credentials()
            except Exception:
                pass

    def get_auth_headers(self):
        """Return authorisation headers."""
        auth_string = self.get_auth_string()
        encoded_auth_string = base64.b64encode(auth_string.encode("utf-8"))
        return {"Authorization": encoded_auth_string}

    def get_auth_string(self):
        """Return the authorisation string for HTTP request headers."""
        if self.use_staging is True:
            return "{}:{}".format(self.staging_key, self.staging_secret_token)
        else:
            return "{}:{}".format(self.live_key, self.live_secret_token)

    @property
    def domain(self):
        """Return the domain to which HTTP requests will be made."""
        if self.use_staging is True:
            return self.STAGING_DOMAIN
        elif self.use_staging is False:
            return self.LIVE_DOMAIN
        else:
            raise ValueError(
                "Domain not set. Please set pywowcher.session.staging to True or False"
            )

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
        credentials_path = self.get_wowcher_credentials_file()
        if credentials_path is None:
            logging.error("Wowcher credentials file not found.")
            raise FileNotFoundError(
                "{} was not found.".format(self.WOWCHER_CREDENTIALS_FILENAME)
            )
        else:
            logger.debug("Credentials file found at {}".format(credentials_path))
            self.load_credentials_from_file(credentials_path)

    def load_credentials_from_file(self, credentials_path):
        """Add API credentials from file."""
        logger.info("Loading API Credentials from {}".format(credentials_path))
        with open(credentials_path, "r") as config_file:
            config = yaml.load(config_file)
        try:
            if self.live_key is None:
                self.live_key = config["live"]["key"]
            if self.live_secret_token is None:
                self.live_secret_token = config["live"]["secret_token"]
            if self.staging_key is None:
                self.staging_key = config["staging"]["key"]
            if self.staging_secret_token is None:
                self.staging_secret_token = config["staging"]["secret_token"]
            if self.use_staging is None:
                self.use_staging = config["use_staging"]
        except Exception as e:
            logger.error("Could not load config from {}.".format(credentials_path))
            raise e

    def set_credentials(
        self,
        live_key=None,
        live_secret_token=None,
        live_staging=None,
        staging_key=None,
        staging_secret_token=None,
        staging_staging=None,
        use_staging=None,
    ):
        """
        Set the API key, secret token and domain to use for API requests.

        :param key str: Your Wowcher API key.
        :param secret_token str: Your Wowcher API token.
        :param staging bool: If True API requests will address the staging server, if it
            is False the live server will be addresed.
        """
        for key, value in locals().items():
            if value is not None:
                setattr(self, key, value)

    def create_credentials_file(
        self,
        *,
        live_key,
        live_secret_token,
        staging_key,
        staging_secret_token,
        use_staging
    ):
        """
        Create an API credential file.

        This file will be named `wowcher_credentials.yaml` and saved in the current
        working directory.

        When this file is in the current working directory or one of it's ancestors the
        credentials and domain it specifies will be used by `pywowcher` for API requests
        unless overriden by a call to :attr:`pywowcher.session.set_credentials`.

        :param key str: Your Wowcher API key.
        :param secret_token str: Your Wowcher API token.
        :param staging bool: If True API requests will address the staging server, if it
            is False the live server will be addresed.
        """
        path = os.path.join(os.getcwd(), self.WOWCHER_CREDENTIALS_FILENAME)
        live = {"key": live_key, "secret_token": live_secret_token}
        staging = {"key": staging_key, "secret_token": staging_secret_token}
        config = {"live": live, "staging": staging, "use_staging": use_staging}
        with open(path, "w") as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

    def clear(self):
        """Clear the session credentials."""
        self.live_key = None
        self.live_secret_token = None
        self.staging_key = None
        self.staging_secret_token = None
        self.use_staging = None


session = WowcherAPISession()
