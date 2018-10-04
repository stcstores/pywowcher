Getting Started
===============

Installation
------------

To install pywowcher you can clone this repository and install using pip::

  git clone https://github.com/lukeshiner/pywowcher.git
  cd pywowcher
  pip install -e .

Pywowcher will be available on PyPI once feature-complete.


Connecting to Wowcher
---------------------

In order to use Wowcher you will need credentials to access the Wowcher API. These can
be requested from Wowcher. Access credentials are managed in `pywowcher` with
an instance of :class:`pywowcher.wowcher_session.WowcherAPISession`, accessed by
:attr:`pywowcher.session`. Use
:func:`pywowcher.wowcher_session.WowcherAPISession.set_credentials` to add your
credentials to pywowcher.

  >>> import pywowcher
  >>> pywowcher.set_credentials(key=YOUR_WOWCHER_KEY, secret_token=YOUR_SECRET_TOKEN)

If no credentials are set `pywowcher` will look for a file named
`wowcher_credentials.yaml` in the current working directory and recursively up from there.
This is a YAML formatted file containing your Wowcher API key and secret token. You can
create one using :func:`pywowcher.session.create_credentials_file`::

  key: YOU_WOWCHER_KEY
  secret_token: YOUR_SECRET_TOKEN

Use :func:`pywowcher.wowcher_session.WowcherAPISession.set_credentials` if you want to
override an existing `wowcher_credentials.yaml`.


.. autoclass:: pywowcher.wowcher_session.WowcherAPISession

  .. automethod:: set_credentials
  .. automethod:: create_credentials_file
  .. automethod:: clear
