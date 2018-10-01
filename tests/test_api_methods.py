"""Tests for Pywowcher API methods."""

import datetime

import pywowcher

from .basetests import BasePywowcherTest


class TestBaseAPIMethod(BasePywowcherTest):
    """Tests for the base APIMethod class."""

    TEST_URI = "test_uri"

    def get_test_api_method(self, uri, method):
        """Return a new API method."""
        API_method = pywowcher.api_methods.api_method.BaseAPIMethod
        API_method.uri = uri
        API_method.method = method
        return API_method

    def test_method_get_URL(self):
        """Test the get_URL method of BaseAPIMethod."""
        expected_URL = f"{pywowcher.WowcherAPISession.DOMAIN}{self.TEST_URI}"
        API_method = self.get_test_api_method(
            self.TEST_URI, pywowcher.api_methods.api_method.BaseAPIMethod.POST
        )
        assert expected_URL == API_method.get_URL()

    def test_post_request(self, requests_mock):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(
            self.TEST_URI, pywowcher.api_methods.api_method.BaseAPIMethod.POST
        )
        requests_mock.post(API_method.get_URL(), text=response_text)
        response = API_method().call()
        assert response.text == response_text

    def test_get_request(self, requests_mock):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(
            self.TEST_URI, pywowcher.api_methods.api_method.BaseAPIMethod.GET
        )
        requests_mock.register_uri("GET", API_method.get_URL(), text=response_text)
        response = API_method().call()
        assert response.text == response_text


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
    DEAL_ID = 9_856_321

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
                "timestamp": 1_234_567_890,
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
