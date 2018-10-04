"""Pywowcher - A Wowcher API integration for Python."""

from .__version__ import __title__, __description__, __url__  # NOQA
from .__version__ import __version__, __author__, __author_email__  # NOQA
from .__version__ import __copyright__, __license__, __release__  # NOQA

import logging
from .wowcher_session import session  # NOQA
from . import api_methods  # NOQA
from .operations.echotest import echo_test  # NOQA
from .operations.getorders import get_orders, WowcherOrder, WowcherItem  # NOQA
from .operations.setorderstatus import set_order_status, make_order_status  # NOQA

logging.getLogger(__name__).addHandler(logging.NullHandler())

REFERENCE = api_methods.Status.REFERENCE
STATUS = api_methods.Status.STATUS
TIMESTAMP = api_methods.Status.TIMESTAMP
TRACKING_NUMBER = api_methods.Status.TRACKING_NUMBER
SHIPPING_VENDOR = api_methods.Status.SHIPPING_VENDOR
SHIPPING_METHOD = api_methods.Status.SHIPPING_METHOD

RECIEVED_BY_MERCHANT = api_methods.Status.RECIEVED_BY_MERCHANT
READY_FOR_DISPATCH = api_methods.Status.READY_FOR_DISPATCH
DISPATCHED = api_methods.Status.DISPATCHED
