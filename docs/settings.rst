Settings
===========

Some of Django REST Framework Simple API Key's behavior can be customized through settings variables in
``settings.py``. You can find below the default `SIMPLE_API_KEY` setting.

.. code-block:: python

  # Django project settings.py
  ...

  SIMPLE_API_KEY = {
       "FERNET_SECRET": "",
       "API_KEY_LIFETIME": 365,
       "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
  }


Above, the default values for these settings are shown.

``FERNET_SECRET``
-------------------------
The fernet key (`Fernet <https://cryptography.io/en/latest/fernet/>`__) is used to encrypt and decrypt API Keys.

To generate a fresh fernet key, you can use the following command:

 python manage.py generate_fernet_key

Make sure to store it somewhere safe and treat it as you will treat the ``SECRET_KEY`` Django setting.

``API_KEY_LIFETIME``
--------------------------

Determines the validity period of a generated Api Key. The default value is 365 days. 

``AUTHENTICATION_KEYWORD_HEADER``
----------------------------

Determines the keyword that should come with every request made to your API. The default value is ``Api-Key`` and it is used in the following format:

 Api-Key API_KEY
