"""
The set_order_status method of pywocher.

Used to update the status of on or more orders.
"""

from pywowcher import api_methods


class SetOrderStatus:
    """Set the status of one or more orders."""

    REFERENCE = api_methods.Status.REFERENCE
    STATUS = api_methods.Status.STATUS
    TIMESTAMP = api_methods.Status.TIMESTAMP
    TRACKING_NUMBER = api_methods.Status.TRACKING_NUMBER
    SHIPPING_VENDOR = api_methods.Status.SHIPPING_VENDOR
    SHIPPING_METHOD = api_methods.Status.SHIPPING_METHOD

    def __init__(self, *, orders):
        """
        Set the status of one or more orders.

        :param orders: list containing dicts of orders formatted for a status update.
            These can be created with :func:`pywowcher.make_order_status`.
        """
        self.orders_to_send = []
        for order_number, order in enumerate(orders):
            try:
                self.orders_to_send.append(self.prepare_order(order))
            except Exception:
                raise ValueError(
                    "Invalid order for status update at index {}".format(order_number)
                )
        api_methods.Status(orders=orders).call()

    def prepare_order(self, order):
        """Return a dict correctly formatted for an order for the Status API method."""
        order_dict = {
            self.REFERENCE: order[self.REFERENCE],
            self.STATUS: order[self.STATUS],
        }
        if self.TIMESTAMP in order:
            order_dict[self.TIMESTAMP] = order[self.TIMESTAMP]
        if self.TRACKING_NUMBER in order:
            order_dict[self.TRACKING_NUMBER] = order[self.TRACKING_NUMBER]
        if self.SHIPPING_VENDOR in order:
            order_dict[self.SHIPPING_VENDOR] = order[self.SHIPPING_VENDOR]
        if self.SHIPPING_METHOD in order:
            order_dict[self.SHIPPING_METHOD] = order[self.SHIPPING_METHOD]
        return order_dict


def make_order_status(
    *,
    reference,
    status,
    timestamp=None,
    tracking_number=None,
    shipping_vendor=None,
    shipping_method=None,
):
    """
    Return an order formatted for the set_order_status operation.

    Format an order for the set_order_status operation. This can be passed to
    set_order_status as part of an iterable.

    :param reference: The wowcher reference code for the order
        (:attr:`pywowcher.WowcherOrder.reference`).
    :type reference: int or str

    :param status: The updated status of the order. Can be
        :attr:`pywowcher.RECIEVED_BY_MERCHANT`, :attr:`pywowcher.READY_FOR_DISPATCH` or
        :attr:`pywowcher.DISPATCHED`.
    :type status: str

    :param timestamp: The time at which the order status changed. If None is passed the
        current time will be used.
    :type timestamp: :class:`datetime.datetime` or None

    :param tracking_number: The tracking number for the shipment. Use None if not
        applicable.
    :type tracking_number: str or None

    :param shipping_vendor: The shipping provider carring the shipment. Can be None.
    :type shipping_vendor: str or None

    :param shipping_method: The service used to ship the order. Can be None.
    :type shipping_method: str or None

    :rtype dict:
    """
    return {
        SetOrderStatus.REFERENCE: reference,
        SetOrderStatus.STATUS: status,
        SetOrderStatus.TIMESTAMP: timestamp,
        SetOrderStatus.TRACKING_NUMBER: tracking_number,
        SetOrderStatus.SHIPPING_VENDOR: shipping_vendor,
        SetOrderStatus.SHIPPING_METHOD: shipping_method,
    }


def set_order_status(orders):
    """
    Set the status of one or more orders.

    :param orders: list containing dicts of orders formatted for a status update. These
        can be created with :func:`pywowcher.make_order_status`.
    """
    SetOrderStatus(orders=orders)
