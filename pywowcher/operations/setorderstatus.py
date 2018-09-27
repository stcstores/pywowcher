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

        Kwargs:
            orders: list containing dicts of order parameters in the form:
                {
                    pywowcher.REFERENCE: The Wowcher Code, e.g., 8UPGT3-KKQRNC,
                    pywowcher.STATUS: The updated status of the order, choose from
                        pywowcher.RECIEVED_BY_MERCHANT, pywowcher.READY_FOR_DISPATCH or
                        pywowcher.DISPATCHED,
                    pywowcher.TIMESTAMP: The Unix Timestamp of the update (optional,
                        defaults to the time of the request),
                    pywowcher.TRACKING_NUMBER: The tracking number (optional),
                    pywowcher.SHIPPING_VENDOR: The courier used to ship the order
                        (optional),
                    pywowcher.SHIPPING_METHOD: The courier shipping method used to ship
                        the order (optional),
                }
        """
        self.orders_to_send = []
        for order_number, order in enumerate(orders):
            try:
                self.orders_to_send.append(self.prepare_order(order))
            except Exception:
                raise ValueError(
                    f"Invalid order for status update at index {order_number}"
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


def set_order_status(orders):
    """
    Set the status of one or more orders.

    Kwargs:
        orders: list containing dicts of order parameters in the form:
            {
                pywowcher.REFERENCE: The Wowcher Code, e.g., 8UPGT3-KKQRNC,
                pywowcher.STATUS: The updated status of the order, choose from
                    pywowcher.RECIEVED_BY_MERCHANT, pywowcher.READY_FOR_DISPATCH or
                    pywowcher.DISPATCHED,
                pywowcher.TIMESTAMP: The Unix Timestamp of the update (optional,
                    defaults to the time of the request),
                pywowcher.TRACKING_NUMBER: The tracking number (optional),
                pywowcher.SHIPPING_VENDOR: The courier used to ship the order
                    (optional),
                pywowcher.SHIPPING_METHOD: The courier shipping method used to ship
                    the order (optional),
            }
    """
    SetOrderStatus(orders=orders)
