"""The Orders API method."""
from .api_method import BaseAPIMethod


class Orders(BaseAPIMethod):
    """
    The Orders API method.

    Returns a page of orders for a deal ID.

    Kwargs:
        page (int): The number of the page to return.
        per_page (int): The number of orders per page.
        from_date (datetime.datetime): When to retrive orders from.
        start_date (datetime.datetime): Filter orders using a start date.
        end_date (datetime.datetime): Filter orders using an end date.
        deal_id (int): The Wowcher Deal ID to retrive orders for.
    """

    uri = "/v1/orders"
    method = BaseAPIMethod.GET

    def get_data(self, *, page, per_page, from_date, start_date, end_date, deal_id):
        """
        Return data to be passed in the request.

        Kwargs:
            page (int): The number of the page to return.
            per_page (int): The number of orders per page.
            from_date (datetime.datetime): When to retrive orders from.
            start_date (datetime.datetime): Filter orders using a start date.
            end_date (datetime.datetime): Filter orders using an end date.
            deal_id (int): The Wowcher Deal ID to retrive orders for.
        """
        return {
            "page": page,
            "per_page": per_page,
            "from_date": from_date,
            "start_date": start_date,
            "end_date": end_date,
            "deal_id": deal_id,
        }

    def process_response(self, response):
        """Process echo response."""
        return response.json()
