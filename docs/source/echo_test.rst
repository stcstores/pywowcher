Echo Test
=========

To check your connection to the Wowcher servers use :func:`pywowcher.echo_test`. This
function takes an object that can be serialized such as a :class:`list` or :class:`dict`
and sends it as JSON to the Wowcher servers. If no error occurs Wowcher will send an
HTTP response including the sent data, which the function will return unchanged.

  >>> import pywowcher
  >>>
  >>> data = {'One': 1, 'Two': 'two'}
  >>> pywowcher.echo_test(data)
  {'One': 1, 'Two': 'two'}

.. autofunction:: pywowcher.echo_test
