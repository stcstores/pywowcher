"""Pywowcher - A Wowcher API integration for Python."""

import logging
from .session import WowcherAPISession  # NOQA
from . import api_methods  # NOQA
from .operations import echo_test, get_orders  # NOQA

logging.getLogger(__name__).addHandler(logging.NullHandler())
