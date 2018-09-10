"""Tests for Pywowcher API methods."""
import datetime

import pywowcher
import requests_mock
from pywowcher import WowcherAPISession
from pywowcher.api_methods.api_method import BaseAPIMethod

from .pywowcher_test_case import PywowcherTestCase


class TestAPIMethod(PywowcherTestCase):
    """Test the pywowhcer.api_methods.api_method.BaseAPIMethod class."""

    TEST_URI = "test_uri"

    def get_test_api_method(self, uri, method):
        """Return a new API method."""
        API_method = BaseAPIMethod
        API_method.uri = uri
        API_method.method = method
        return API_method

    def test_method_get_URL(self):
        """Test the get_URL method of BaseAPIMethod."""
        expected_URL = f"{WowcherAPISession.DOMAIN}{self.TEST_URI}"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.POST)
        self.assertEqual(expected_URL, API_method.get_URL())

    @requests_mock.mock()
    def test_post_request(self, m):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.POST)
        m.post(API_method.get_URL(), text=response_text)
        response = API_method().call()
        self.assertEqual(response.text, response_text)

    @requests_mock.mock()
    def test_get_request(self, m):
        """Test the WowcherAPISession.make_request method."""
        response_text = "hello"
        API_method = self.get_test_api_method(self.TEST_URI, BaseAPIMethod.GET)
        m.get(API_method.get_URL(), text=response_text)
        response = API_method().call()
        self.assertEqual(response.text, response_text)


class TestEchoTestMethod(PywowcherTestCase):
    """Test the EchoTest API method."""

    MESSAGE = {"one": "1", "two": "2"}
    RESPONSE = {"message": "Echo Test Received", "data": MESSAGE}
    API_METHOD = pywowcher.api_methods.EchoTest

    @requests_mock.mock()
    def test_echo_test_method(self, m):
        """Test the EchoTest API method."""
        m.post(self.API_METHOD.get_URL(), json=self.RESPONSE)
        response = self.API_METHOD(self.MESSAGE).call()
        self.assertEqual(response, self.MESSAGE)


class TestOrdersMethod(PywowcherTestCase):
    """Test the Orders API method."""

    PAGE = 1
    PER_PAGE = 100
    FROM_DATE = datetime.datetime.now() - datetime.timedelta(days=1)
    START_DATE = datetime.datetime.now() - datetime.timedelta(days=1)
    END_DATE = datetime.datetime.now()
    DEAL_ID = 1

    RESPONSE = {
        "total": 500,
        "per_page": 100,
        "current_page": 1,
        "last_page": 5,
        "from": 1,
        "to": 100,
        "data": [
            {
                "id": 772601,
                "business_id": 269272,
                "merchant_id": 720033,
                "deal_id": 481790,
                "wowcher_code": "8UPGT3-KKQRNC",
                "brand": 0,
                "redeemed_at": 1503432923,
                "received_at": 1503433923,
                "ready_for_despatch_at": 1503433943,
                "despatched_at": 1503434023,
                "product": {
                    "code": 9413,
                    "name": "Happy Teddy Bear",
                    "sku": "481790-9413",
                    "despatch_method": 182,
                    "options": "",
                },
                "delivery_address": {
                    "title": "Mr",
                    "first_name": "Mitch",
                    "last_name": "Trubisky",
                    "line_1": "4 Soldier Way",
                    "line_2": "",
                    "city": "London",
                    "county": "",
                    "postcode": "SW1A 1AA",
                    "country": "GB",
                    "telephone": "01632 960708",
                    "email": "mitch@example.com",
                },
            }
        ],
    }

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
        self.assertEqual(method.data, expected_data)

    @requests_mock.mock()
    def test_process_response_method(self, m):
        """Test the process_response method of Orders."""
        m.get(pywowcher.api_methods.Orders.get_URL(), json=self.RESPONSE)
        response = pywowcher.api_methods.Orders(
            page=self.PAGE,
            per_page=self.PER_PAGE,
            from_date=self.FROM_DATE,
            start_date=self.START_DATE,
            end_date=self.END_DATE,
            deal_id=self.DEAL_ID,
        ).call()
        self.assertEqual(response, self.RESPONSE)
