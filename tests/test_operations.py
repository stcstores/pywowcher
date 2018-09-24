"""Tests for pywowhcer's main methods."""

import pywowcher

from . import test_api_methods


def test_echo_test_operation(requests_mock):
    """Test the EchoTest operation."""
    message = {"one": "1", "two": "2"}
    test_api_methods.mock_echo_test(requests_mock, message)
    assert pywowcher.echo_test(message) == message


def test_get_orders_returns_list_of_wowcher_orders(requests_mock):
    """Test the get_orders operation returns a list of WowcherOrder instances."""
    test_api_methods.mock_orders(requests_mock)
    response = pywowcher.get_orders(deal_id=1)
    assert isinstance(response, list)
    assert isinstance(response[0], pywowcher.operations.getorders.WowcherOrder)


def test_get_orders_returns_empty_list_when_there_are_no_orders(requests_mock):
    """Test the get_orders operation returns an empty list when no orders exist."""
    response_data = test_api_methods.orders_method_response()
    response_data["data"]["total"] = 0
    response_data["data"]["data"] = []
    test_api_methods.mock_orders(requests_mock, response_data=response_data)
    response = pywowcher.get_orders(deal_id=1)
    assert response == []


def test_get_orders_handles_pagination(requests_mock):
    """Test the get_orders operation handles paginated responses."""
    pages = 3
    base_response = test_api_methods.orders_method_response()
    base_response["data"]["total"] = pages * 100
    base_response["data"]["last_page"] = pages
    responses = [dict(base_response) for _ in range(pages)]
    for response_number, response in enumerate(responses):
        response["data"]["current_page"] = response_number + 1
    response = [{"json": response} for response in responses]
    test_api_methods.mock_orders(requests_mock, response=response)
    returned_value = pywowcher.get_orders(deal_id=1)
    assert isinstance(returned_value, list)
    assert len(returned_value) == 300


def test_wowcher_order_repr():
    """Test the wowcher order __repr__ method."""
    order_data = test_api_methods.orders_method_response()["data"]["data"][0]
    order = pywowcher.operations.getorders.WowcherOrder(order_data)
    wowcher_code = order_data["wowcher_code"]
    assert order.__repr__() == f"Wowcher Order {wowcher_code}"
