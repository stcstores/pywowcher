"""Pywowcher - A Wowcher API integration for Python."""

import logging
from .wowcher_session import session  # NOQA
from . import api_methods  # NOQA
from .operations import echo_test, get_orders, set_order_status  # NOQA

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
