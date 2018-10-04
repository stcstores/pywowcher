"""
The operations package contains the primary pywowcher functions.

These are the methods used to communicate with Wowcher.
"""

from .echotest import echo_test  # NOQA
from .getorders import get_orders  # NOQA
from .setorderstatus import set_order_status, make_order_status  # NOQA
