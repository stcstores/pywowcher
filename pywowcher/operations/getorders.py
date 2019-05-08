"""
The get_orders method of pywowcher.

Used to retrieve orders from Wowcher. It returns a list of orders encapsulated by the
WowcherOrder class.
"""

import datetime

from pywowcher import api_methods


class WowcherItem:
    """
    A wrapper for Wowcher order items as returned from an Order API request.

    :ivar str sku: The product's stock keeping unit (SKU).
    :ivar int quantity: The quantity of the item ordered.
    :ivar str options: The product options selected by the customer.
    """

    SKU = "sku"
    QUANTITY = "quantity"
    OPTIONS = "options"

    def __init__(self, item_data):
        """
        Set item attributes.

        :param item_data: One item from a Wowcher order as returned from an Orders API
            request.
        :type item_data: dict
        """
        self.sku = item_data[self.SKU]
        self.quantity = item_data[self.QUANTITY]
        self.options = item_data[self.OPTIONS]

    def __repr__(self):
        return "Wowcher item {}".format(self.sku)


class WowcherOrder:
    """
    A wrapper for Wowcher orders as returned from an Order API request.

    :ivar items list: The items that were ordered as instances of
        :class:`pywowcher.WowcherItem`.
    :type items: list
    :ivar brand: The brand of the deal.
    :ivar business_id: Your business ID.
    :ivar created_at: The time at which the order was created as a UNIX timestamp.
    :ivar currency: Currency code for the currency used to pay for the item. E.g "GBP".
    :ivar custom_field: Custom item information.
    :ivar deal_id: The ID of the deal the order belongs to.
    :ivar delivery_city: The city of the customer's address.
    :ivar delivery_country: The country of the customer's address.
    :ivar delivery_email: The customer's email address.
    :ivar delivery_first_name: The customer's first name.
    :ivar delivery_last_name: The customer's last name.
    :ivar delivery_line_1: The first line of the customer's address.
    :ivar delivery_line_2: The second line of the customer's address.
    :ivar delivery_postcode: The customer's postal or zip code.
    :ivar delivery_telephone: The customer's contact phone number.
    :ivar delivery_title: The customer's title. E.g 'Mr'.
    :ivar despatched_at: The time at which the item was dispatched as a UNIX timestamp.
    :ivar full_price: The full price of the order.
    :ivar merchant_id: Your Wowcher merchant ID.
    :ivar price: The price of the item.
    :ivar product_code: Wowcher's reference code for the product.
    :ivar product_name: The name of the sold product.
    :ivar product_options: A comma-separated string of options such as colour, size.
    :ivar product_sku: Your SKU for the sold product.
    :ivar ready_for_despatch_at: Time at which the order was marked at ready for
        dispatch as a UNIX timestamp.
    :ivar received_at: Time at which the order was recieved as a UNIX timestamp.
    :ivar redeemed_at: Time at which the order was redeemed as a UNIX timestamp.
    :ivar sent_at: Time at which the order was sent as a UNIX timestamp.
    :ivar shipping_method: The method used to ship the order.
    :ivar shipping_vendor: The shipping provider used to ship the order.
    :ivar tracking_number: The tracking number for the shipment.
    :ivar updated_at: Time at which the order was last updated as a UNIX timestamp.
    :ivar wowcher_code: Wowcher's reference code for the order.
    """

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
        """
        Set order attributes.

        :param order_data: Data for one order as returned from an Orders API request.
        :type order_data: dict
        """
        self.order_id = order_data["id"]
        self.items = [WowcherItem(item_data) for item_data in order_data["items"]]
        for field in self.fields:
            setattr(self, field, order_data[field])

    def __repr__(self):
        return "Wowcher Order {}".format(self.wowcher_code)


class GetOrders:
    """Request all pages for an Orders API method call and collect the orders."""

    PER_PAGE = 100
    LAST_PAGE = "last_page"
    DATA = "data"

    def __init__(self, *, deal_id, from_date=None, start_date=None, end_date=None):
        """
        Request all pages for an Orders API method call and collect the orders.

        :param deal_id: The ID of the Wowcher deal for which to collect orders.
        :type deal_id: str or int

        :param from_date: When to retrieve orders from.
        :type from_date: datetime.datetime

        :param start_date: Filter orders using a start date.
        :type start_date: datetime.datetime

        :param end_date: Filter orders using a end date.
        :type end_date: datetime.datetime

        :ivar orders: orders: A list containing the requested orders as
            :class:`pywowcher.WowcherOrder`.
        :type orders: list

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
        for page in range(2, self.page_count + 1):
            self.add_orders(self.make_order_request(page))

    def first_request(self):
        """Make an Orders request, store the page count and process the response data."""
        response_data = self.make_order_request(1)
        self.page_count = response_data[self.DATA][self.LAST_PAGE]
        self.add_orders(response_data)

    def add_orders(self, response_data):
        """
        Add the orders from a the response to an Orders request to self.orders.

        :param response_data: Returned data from an Orders API requset.
        :type response_data: dict
        """
        orders = response_data[self.DATA][self.DATA]
        for order in orders:
            self.orders.append(self.process_order_data(order))

    def process_order_data(self, order_data):
        """
        Return Wowcher order data as :class:`pywowcher.WowcherOrder`.

        :param order_data: Order data as returned from an Orders API request for a
            single order.
        :type order_data: dict

        :rtype: :class:`pywowcher.WowcherOrder`
        """
        return WowcherOrder(order_data)

    def make_order_request(self, page):
        """
        Return the response to an Orders request for a page of orders.

        :pram page: Page number to request.
        :type page: int

        :rtype: dict
        """
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
    Return a list of customer orders for a Wowcher deal.

    :param deal_id: The ID of the Wowcher deal for which to collect orders.
    :type deal_id: int or str

    :param from_date: When to retrieve orders from.
    :type from_date:  :class:`datetime.datetime` or None

    :param start_date: Filter orders using a start date.
    :type start_date:  :class:`datetime.datetime` or None

    :param end_date: Filter orders using a end date.
    :type end_date:  :class:`datetime.datetime` or None

    :rtype: :class:`pywowcher.WowcherOrder`

    """
    return GetOrders(
        deal_id=deal_id, from_date=from_date, start_date=start_date, end_date=end_date
    ).orders
