Settings
===========

Some of Simple API Key's behavior can be customized through settings variables in
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
`Fernet <https://cryptography.io/en/latest/fernet/>`__ guarantees that a message encrypted using it can not be manipulated or read without the key.

To generate a fresh fernet key, you can use the following command:

 python manage.py generate_fernet_key

Keep it safe and save it in your code as an environment variable.

``API_KEY_LIFETIME``
--------------------------

Determines the validity period of a generated Api Key

``AUTHENTICATION_MODEL``
-------------------------

Indicates the model associated to the API Keys.

``AUTHENTICATION_KEYWORD_HEADER``
----------------------------

Determines the keyword that should come with every request made to your API. By default it will be in the following format:
 Api-Key 3z1Z1axT8ayiGAjF7g42Cfjtg8TYDndiEqzOQTewWu0
