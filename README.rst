.. image:: https://travis-ci.org/lukeshiner/pywowcher.svg?branch#master
    :target: https://travis-ci.org/lukeshiner/pywowcher

.. image:: https://coveralls.io/repos/github/lukeshiner/pywowcher/badge.svg?branch#ci-coveralls
    :target: https://coveralls.io/github/lukeshiner/pywowcher?branch#ci-coveralls

.. image:: https://readthedocs.org/projects/pywowcher/badge/?version=latest
    :target: https://pywowcher.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


#########################################
Pywowcher - Wowcher API Client for Python
#########################################

Note: This project is under development. Do not use in production.

Features
========

Pywowcher allows you to:

- Retrieve orders for a current deal.
- Update the status of an order.
- Make an echo test to the Wowcher server.

Installation
============
To install pywowcher you can clone this repository and install using pip::

  git clone https://github.com/lukeshiner/pywowcher.git
  cd pywowcher
  pip install -e .

Pywowcher will be available on PyPI once feature-complete.

Basic Usage
===========

Getting started::

  >>> import pywowcher
  >>>
  >>> pywowcher.set_credentials(key="YOUR_API_KEY", secret_token="YOUR_SECRET_TOKEN")

Retrieving orders::

  >>> orders = pywowcher.get_orders(deal_id="YOUR_DEAL_ID")
  >>> print(orders)
  [Wowcher Order VXF7YW-PDWZC9, Wowcher Order XH8CZY-OEXFZ9]


Updating order status::

  >>> order_status = pywowcher.make_order_status(
  ...   reference=orders[0].wowcher_code, status=pywowhcer.DISPATCHED
  ... )
  >>> pywowcher.set_order_status([order_status])
  >>>

Testing API access::

  >>> pywowcher.echo_test({'test_key_1': 'test_value_1', 'test_key_2': 2})
  {'test_key_1': 'test_value_1', 'test_key_2': 2}
