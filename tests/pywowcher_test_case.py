"""PywowcherTestCase, base class for pywowcher test cases."""

import os
import shutil
import tempfile
import unittest

from pywowcher import WowcherAPISession


class PywowcherTestCase(unittest.TestCase):
    """Base class for Pywowcher tests."""

    key = "0ff52fd6-7860-4f07-bab5-5fa74d3b98f0"
    secret_token = "16459c82-065a-4e51-b682-c784e404831d"

    def setUp(self):
        """Create a temporary working directory."""
        self.create_working_directory()

    def tearDown(self):
        """Delete the temporary working directory."""
        self.remove_working_directory()
        self.reset_session_class()

    def reset_session_class(self):
        """Reset the class attributes of the session class."""
        WowcherAPISession.key = None
        WowcherAPISession.secret_token = None

    def create_working_directory(self):
        """Set the working directory to a temp dir and create a credentials file."""
        os.chdir(tempfile.mkdtemp())
        WowcherAPISession.create_credentials_file(
            key=self.key, secret_token=self.secret_token
        )

    def remove_working_directory(self):
        """Remove the temporary working directory."""
        shutil.rmtree(str(os.path.abspath(os.getcwd())))
