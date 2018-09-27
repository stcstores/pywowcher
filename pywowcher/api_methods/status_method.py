"""The Status API mehtod."""

from .api_method import BaseAPIMethod


class Status(BaseAPIMethod):
    """
    The Status API method.

    Used to update the status of one or more orders.

    Kwargs:
        orders: list containing dicts of order parameters in the form:
            {
                "reference": The Wowcher Code, e.g., 8UPGT3-KKQRNC,
                "timestamp": The Unix Timestamp of the update (optional, defaults to
                    the time of the request),
                "status": The updated status of the order; Status.RECIEVED_BY_MERCHANT,
                    Status.READY_FOR_DISPATCH or Status.DISPATCHED,
                "tracking_number": The courier supplied tracking number (optional),
                "shipping_vendor": The courier used to ship the order (optional),
                "shipping_method": The courier shipping method used to ship the order
                    (optional),
            }
    """

    uri = "/v1/orders/status"
    method = BaseAPIMethod.PUT

    RECIEVED_BY_MERCHANT = 0
    READY_FOR_DISPATCH = 1
    DISPATCHED = 2

    ORDERS = "orders"

    def get_data(self, *, orders):
        """Return data to be passed to the request."""
        return {self.ORDERS: orders}
