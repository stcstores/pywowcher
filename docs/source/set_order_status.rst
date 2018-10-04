Set Order Status
================

Use :func:`pywowcher.set_order_status` to update the status of an order. This takes a
:class:`list` of :class:`dict` containing details of the status update. This can be
created using :func:`pywowcher.make_order_status`.

  >>> update_1 = pywowcher.make_order_status(
  ...   reference="8UPGT3-KKQRNC",
  ...   status=pywowcher.DISPATCHED,
  ...   timestamp=1538651896,
  ...   tracking_number="GB1589432_A",
  ...   shipping_vendor="ROYAL_MAIL",
  ...   shipping_method="NEXT_DAY",
  ... )
  >>> update_2 = pywowcher.make_order_status(
  ...   reference="YA9APE-492D9N", status=pywowhcer.RECIEVED_BY_MERCHANT
  ... )
  >>> pywowcher.set_order_status([update_1, update_2])

Alternativly the update :class:`dict` can be created manually.

  >>> order_data = {
  ...   pywowcher.REFERENCE: "8UPGT3-KKQRNC",
  ...   pywowcher.STATUS: pywowcher.DISPATCHED,
  ...   pywowcher.TIMESTAMP: 1538651896,
  ...   pywowcher.TRACKING_NUMBER: "GB1589432_A",
  ...   pywowcher.SHIPPING_VENDOR: "ROYAL_MAIL",
  ...   pywowcher.METHOD: "NEXT_DAY",
  ... }
  >>> pywowcher.set_order_status(order_data)

The parameters are:

- :attr:`pywowcher.REFERENCE`: The Wowcher reference code for the order. This can be
  found in :attr:`pywowcher.WowcherOrder.reference`.
- :attr:`pywowcher.STATUS`: The updated status of the order. The options for this are:

  + :attr:`pywowcher.RECIEVED_BY_MERCHANT`: Acknowledge that you have recieved the order
  + :attr:`pywowcher.READY_FOR_DISPATCH`: The order has been processed and is ready to
    be shipped.
  + :attr:`pywowcher.DISPATCHED`: The order has been shipped.

- :attr:`pywowcher.TIMESTAMP`: The Unix Timestamp of the update (optional, defaults to
  the time of the request).
- :attr:`pywowcher.TRACKING_NUMBER`: The courier supplied tracking number (optional).
- :attr:`pywowcher.SHIPPING_VENDOR`: The courier used to ship the order (optional).
- :attr:`pywowcher.METHOD`: The courier shipping method used to ship the order (optional).

.. autofunction:: pywowcher.set_order_status

.. autofunction:: pywowcher.make_order_status
