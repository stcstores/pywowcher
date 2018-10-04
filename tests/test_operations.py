"""Tests for pywowhcer's main methods."""

import pytest
import pywowcher

from .basetests import BasePywowcherTest


class TestEchoTestOperation(BasePywowcherTest):
    """Tests for the echo_test operation."""

    def test_echo_test_operation(self, mock_echo_test):
        """Test the EchoTest operation."""
        message = {"one": "1", "two": "2"}
        mock_echo_test(message)
        assert pywowcher.echo_test(message) == message


class TestGetOrdersOperation(BasePywowcherTest):
    """Tests for the get_orders operation."""

    def test_get_orders_returns_list_of_wowcher_orders(self, mock_orders):
        """Test the get_orders operation returns a list of WowcherOrder instances."""
        mock_orders()
        response = pywowcher.get_orders(deal_id=1)
        assert isinstance(response, list)
        assert isinstance(response[0], pywowcher.operations.getorders.WowcherOrder)

    def test_get_orders_returns_empty_list_when_there_are_no_orders(
        self, mock_orders, orders_method_response
    ):
        """Test the get_orders operation returns an empty list when no orders exist."""
        response_data = orders_method_response
        response_data["data"]["total"] = 0
        response_data["data"]["data"] = []
        mock_orders(response_data=response_data)
        response = pywowcher.get_orders(deal_id=1)
        assert response == []

    def test_get_orders_handles_pagination(self, mock_orders, orders_method_response):
        """Test the get_orders operation handles paginated responses."""
        pages = 3
        base_response = orders_method_response
        base_response["data"]["total"] = pages * 100
        base_response["data"]["last_page"] = pages
        responses = [dict(base_response) for _ in range(pages)]
        for response_number, response in enumerate(responses):
            response["data"]["current_page"] = response_number + 1
        response = [{"json": response} for response in responses]
        mock_orders(response=response)
        returned_value = pywowcher.get_orders(deal_id=1)
        assert isinstance(returned_value, list)
        assert len(returned_value) == 300

    def test_wowcher_order_repr(self, orders_method_response):
        """Test the wowcher order __repr__ method."""
        order_data = orders_method_response["data"]["data"][0]
        order = pywowcher.operations.getorders.WowcherOrder(order_data)
        wowcher_code = order_data["wowcher_code"]
        assert order.__repr__() == "Wowcher Order {}".format(wowcher_code)


class TestSetOrderStatusOperation(BasePywowcherTest):
    """Tests for the set_order_status operation."""

    def test_set_order_status_operation(self, mock_status):
        """Test the set_order_status operation."""
        mock_status()
        order = pywowcher.make_order_status(
            reference="8UPGT3-KKQRNC",
            timestamp=1234567890,
            status=pywowcher.DISPATCHED,
            tracking_number="JD1233230001012",
            shipping_vendor="ROYAL_MAIL",
            shipping_method="NEXT_DAY",
        )
        orders = [order]
        assert pywowcher.set_order_status(orders) is None

    def test_set_order_status_raises_for_malformed_order(self, mock_status):
        """Test the set_order_status operation raises an exception for an invalid order."""
        mock_status()
        orders = [
            {"reference": "8UPGT3-KKQRNC"}
        ]  # Order data missing the status entry.
        with pytest.raises(ValueError):
            pywowcher.set_order_status(orders)
