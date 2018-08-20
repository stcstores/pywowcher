"""Pywowcher - A Wowcher API integration for Python."""

import logging
from .session import WowcherAPISession  # NOQA
from .api_methods import *  # NOQA

logging.basicConfig(level=logging.DEBUG)
