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

To use pyowcher you will need credentials to access the Wowcher API. These can
be requested from Wowcher. Access credentials are managed in `pywowcher` with
an instance of :class:`pywowcher.wowcher_session.WowcherAPISession`, accessed by
:attr:`pywowcher.session`. Use
:func:`pywowcher.wowcher_session.WowcherAPISession.set_credentials` to add your
credentials to `pywowcher.session`. Wowcher provides two API endpoints, a live endpoint
and a staging endpoint for testing purposes. You can add one or both sets of credentials
with the `set_credentials` method. The use_staging parameter tells pywowcher which set
of credentials to use and which endpoint to address.

  >>> import pywowcher
  >>> pywowcher.set_credentials(
  ...   live_key=YOUR_WOWCHER_KEY, live_secret_token=YOUR_SECRET_TOKEN, use_staging=False)

You can access the Wowcher staging server by passing `staging_key` and
`staging_secret_token` and setting `use_staging` True.

  >>> pywowcher.set_credentials(
  ...   staging_key="YOUR STAGING KEY", staging_secret_token="YOUR STAGING SECRET TOKEN",
  ...   use_staging=True)

If no credentials are set `pywowcher` will look for a file named
`wowcher_credentials.yaml` in the current working directory and recursively up from there.
This is a YAML formatted file containing your Wowcher API key and secret token. You can
create one using :func:`pywowcher.session.create_credentials_file`::

  live:
    key: YOUR_LIVE_KEY
    secret_token: YOUR_LIVE_SECRET_TOKEN
  staging:
    key: YOUR_STAGING_KEY
    secret_token: YOUR_STAGING_SECRET_TOKEN
  use_staging: True

Use :func:`pywowcher.wowcher_session.WowcherAPISession.set_credentials` if you want to
override an existing `wowcher_credentials.yaml`.


.. autoclass:: pywowcher.wowcher_session.WowcherAPISession

  .. automethod:: set_credentials
  .. automethod:: create_credentials_file
  .. automethod:: clear
