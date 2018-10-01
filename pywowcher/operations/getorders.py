"""
The get_orders method of pywowcher.

Used to retrieve orders from Wowcher. It returns a list of orders encapsulated by the
WowcherOrder class.
"""

import datetime

from pywowcher import api_methods


class WowcherItem:
    """A wrapper for Wowcher order items as returned from an Order API request."""

    SKU = "sku"
    QUANTITY = "quantity"
    OPTIONS = "options"

    def __init__(self, item_data):
        """Set item attributes."""
        self.sku = item_data[self.SKU]
        self.quantity = item_data[self.QUANTITY]
        self.options = item_data[self.OPTIONS]


class WowcherOrder:
    """A wrapper for Wowcher orders as returned from an Order API request."""

    fields = (
        "brand",
        "business_id",
        "created_at",
        "currency",
        "custom_field",
        "deal_id",
        "delivery_city",
        "delivery_country",
        "delivery_email",
        "delivery_first_name",
        "delivery_last_name",
        "delivery_line_1",
        "delivery_line_2",
        "delivery_postcode",
        "delivery_telephone",
        "delivery_title",
        "delivery_type",
        "despatched_at",
        "despatched_at_sent",
        "external_reference",
        "full_price",
        "integration_module",
        "merchant_id",
        "merchant_warehouse_key",
        "notification_eligible",
        "price",
        "product_code",
        "product_despatch_method",
        "product_name",
        "product_options",
        "product_sku",
        "ready_for_despatch_at",
        "ready_for_despatch_at_sent",
        "received_at",
        "received_at_sent",
        "redeemed_at",
        "sent_at",
        "shipping_method",
        "shipping_vendor",
        "tracking_number",
        "updated_at",
        "wowcher_code",
    )

    def __init__(self, order_data):
        """Set order attributes."""
        self.order_id = order_data["id"]
        self.items = [WowcherItem(item_data) for item_data in order_data["items"]]
        for field in self.fields:
            setattr(self, field, order_data[field])

    def __repr__(self):
        return f"Wowcher Order {self.wowcher_code}"


class GetOrders:
    """Request all pages for an Orders API method call and collect the orders."""

    PER_PAGE = 100
    LAST_PAGE = "last_page"
    DATA = "data"

    def __init__(self, *, deal_id, from_date=None, start_date=None, end_date=None):
        """
        Request all pages for an Orders API method call and collect the orders.

        Kwargs:
            deal_id: The ID of the Wowcher deal for which to collect orders.
            from_date (datetime.datetime): When to retrieve orders from.
            start_date (datetime.datetime): Filter orders using a start date.
            end_date (datetime.datetime): Filter orders using a end date.

        Attributes:
            orders: A list containing the requested orders.

        """
        if from_date is None:
            from_date = datetime.datetime.now() - datetime.timedelta(days=1)
        if start_date is None:
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
        if end_date is None:
            end_date = datetime.datetime.now()
        self.deal_id = deal_id
        self.from_date = from_date
        self.start_date = start_date
        self.end_date = end_date
        self.orders = []
        self.first_request()
        for page in range(1, self.page_count):
            self.add_orders(self.make_order_request(page))

    def first_request(self):
        """Make an Orders request and process the response data."""
        response_data = self.make_order_request(1)
        self.page_count = response_data[self.DATA][self.LAST_PAGE]
        self.add_orders(response_data)

    def add_orders(self, response_data):
        """Add the orders from a the response to an Orders request to self.orders."""
        orders = response_data[self.DATA][self.DATA]
        for order in orders:
            self.orders.append(self.process_order_data(order))

    def process_order_data(self, order_data):
        """Return a WowcherOrder instance for order_data."""
        return WowcherOrder(order_data)

    def make_order_request(self, page):
        """Request an Orders request for a page of orders and return the result."""
        return api_methods.Orders(
            page=page,
            per_page=self.PER_PAGE,
            from_date=self.from_date,
            start_date=self.start_date,
            end_date=self.end_date,
            deal_id=self.deal_id,
        ).call()


def get_orders(*, deal_id, from_date=None, start_date=None, end_date=None):
    """
    Return a list of Wowcher orders.

    Kwargs:
        deal_id: The ID of the Wowcher deal for which to collect orders.
        from_date (datetime.datetime): When to retrieve orders from.
        start_date (datetime.datetime): Filter orders using a start date.
        end_date (datetime.datetime): Filter orders using a end date.

    Returns:
        list containing WowcherOrder objects.

    """
    return GetOrders(
        deal_id=deal_id, from_date=from_date, start_date=start_date, end_date=end_date
    ).orders
