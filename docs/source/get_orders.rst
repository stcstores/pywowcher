Retrieving Orders
=================

Retrieve orders for a given Wowcher deal with :func:`pywowcher.get_orders`. This will
return a list of orders as instances of :class:`pywowcher.WowcherOrder`. These will
include details of the item sold as :class:`pywowcher.WowcherItem`.

  >>> import pywowcher
  >>>
  >>> orders = pywowcher.get_orders(deal_id=8695919)
  >>> print(orders)
  [Wowcher Order VXF7YW-PDWZC9, Wowcher Order XH8CZY-OEXFZ9]
  >>> print(orders[0].items)
  [Wowcher item 9856321-125487]


.. autofunction:: pywowcher.get_orders

.. autoclass:: pywowcher.WowcherOrder
  :members:

.. autoclass:: pywowcher.WowcherItem
  :members:
