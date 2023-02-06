Settings
===========

Some of Django REST Framework Simple API Key's behavior can be customized through settings variables in
``settings.py``:

.. code-block:: python

  # Django project settings.py

  AUTH_USER_MODEL = "user.User"

  SIMPLE_API_KEY = {
       "FERNET_SECRET": "",
       "API_KEY_LIFETIME": 365,
       "AUTHENTICATION_MODEL": AUTH_USER_MODEL,
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

Determines the validity period of a generated Api Key. The default value is 365 days. After the 365 days, any request made using an expired API key will not be successful.

``AUTHENTICATION_MODEL``
-------------------------

Indicates the model associated to the API Keys. This model is used in the ``APIKey`` model as a ``ForeignKey`` field. It helps identify the entity after authenticating with the API key.

``AUTHENTICATION_KEYWORD_HEADER``
----------------------------

Determines the keyword that should come with every request made to your API. The default value is ``Api-Key`` and it is used in the following format:

 Api-Key API_KEY
