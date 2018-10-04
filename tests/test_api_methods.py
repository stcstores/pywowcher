"""Tests for Pywowcher API methods."""

import datetime

import pywowcher

from .basetests import BasePywowcherTest


class TestEchoTestAPIMethod(BasePywowcherTest):
    """Tests for the Echo Test API method."""

    def test_echo_test_method(self, mock_echo_test):
        """Test the EchoTest API method."""
        message = {"one": "1", "two": "2"}
        mock_echo_test(message)
        response = pywowcher.api_methods.EchoTest(message).call()
        assert response == message


class TestOrdersAPIMethod(BasePywowcherTest):
    """Tests for the Orders API method."""

    PAGE = 1
    PER_PAGE = 100
    FROM_DATE = datetime.datetime.now() - datetime.timedelta(days=1)
    START_DATE = datetime.datetime.now() - datetime.timedelta(days=1)
    END_DATE = datetime.datetime.now()
    DEAL_ID = "9856321"

    def test_Orders_get_data_method(self):
        """Test the get_data method of Orders."""
        method = pywowcher.api_methods.Orders(
            page=self.PAGE,
            per_page=self.PER_PAGE,
            from_date=self.FROM_DATE,
            start_date=self.START_DATE,
            end_date=self.END_DATE,
            deal_id=self.DEAL_ID,
        )
        expected_data = {
            "page": self.PAGE,
            "per_page": self.PER_PAGE,
            "from_date": self.FROM_DATE,
            "start_date": self.START_DATE,
            "end_date": self.END_DATE,
            "deal_id": self.DEAL_ID,
        }
        assert method.data == expected_data

    def test_process_orders_response_method(self, mock_orders, orders_method_response):
        """Test the process_response method of Orders."""
        mock_orders()
        response = pywowcher.api_methods.Orders(
            page=self.PAGE,
            per_page=self.PER_PAGE,
            from_date=self.FROM_DATE,
            start_date=self.START_DATE,
            end_date=self.END_DATE,
            deal_id=self.DEAL_ID,
        ).call()
        assert response == orders_method_response


class TestStatusAPIMethod(BasePywowcherTest):
    """Tests for the Status API method."""

    def test_status_API_method(self, mock_status):
        """Test the Status API method."""
        mock_status()
        orders = [
            {
                "reference": "8UPGT3-KKQRNC",
                "timestamp": 1234567890,
                "status": 2,
                "tracking_number": "JD1233230001012",
                "shipping_vendor": "ROYAL_MAIL",
                "shipping_method": "NEXT_DAY",
            }
        ]
        request = pywowcher.api_methods.Status(orders=orders)
        assert pywowcher.api_methods.Status.ORDERS in request.json
        assert request.json[request.ORDERS][0]["reference"] == orders[0]["reference"]
        response = request.call()
        assert response.status_code == 200
