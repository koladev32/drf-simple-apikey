Settings
===========

Some of Django REST Framework Simple API Key's behavior can be customized through settings variables in
``settings.py``. You can find below the default `DRF_API_KEY` setting.

.. code-block:: python

  # Django project settings.py
  ...

  DRF_API_KEY = {
       "FERNET_SECRET": "",
       "API_KEY_LIFETIME": 365,
       "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
       "ROTATION_PERIOD": timedelta(days=7),
       "ROTATION_FERNET_SECRET": "",
       "IGNORED_ROUTES": ["/admin/"]  # Routes that should be ignored by API key authentication
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

``ROTATION_FERNET_SECRET``
-------------------------
The ``ROTATION_FERNET_SECRET`` is a secondary Fernet key (`Fernet <https://cryptography.io/en/latest/fernet/>`__)
utilized within the ``MultiFernet`` cryptographic scheme.
While the primary Fernet key (**fernet_key**) is used for the main encryption and decryption,
the ``ROTATION_FERNET_SECRET`` plays a pivotal role during key rotation phases.

In the context of ``MultiFernet``:

- New tokens are encrypted using the ``ROTATION_FERNET_SECRET``.
- Tokens can be decrypted with either the ``ROTATION_FERNET_SECRET`` enabling a smooth key rotation without rendering existing tokens obsolete.

 python manage.py generate_fernet_key

This strategic usage ensures that as you transition to a new key, older tokens encrypted with the previous key remain valid, and new tokens are encrypted using the new key.
Thus, a seamless transition is achieved, enhancing security without causing disruptions.

``IGNORED_ROUTES``
-------------------------
A list of URL paths that should be ignored by the API Key Analytics Middleware. Any request to a path that starts with any of these routes will not be tracked in the analytics. The default value is ``["/admin/"]``. This setting is specifically used by the analytics middleware to determine which routes should be excluded from usage tracking.

Example:
.. code-block:: python

  DRF_API_KEY = {
      "IGNORED_ROUTES": [
          "/admin/",  # Excludes admin panel routes from analytics
          "/api/documents/",  # Excludes document API routes from analytics
          "/health/",  # Excludes health check endpoints from analytics
      ]
  }

``ENFORCE_HTTPS``
-------------------------

By default, we enforce HTTPS connections in production to prevent API keys from
being transmitted over unencrypted HTTP. If someone tries to use an API key over
HTTP, the request will be rejected.

**Default:** ``None`` (auto-detects: ``True`` in production when ``DEBUG=False``, ``False`` in development or test environments)

**Example:**

.. code-block:: python

   DRF_API_KEY = {
       "ENFORCE_HTTPS": True,  # Reject HTTP requests in production
   }

**Note:** ⚠️ Always set this to ``True`` in production! Sending API keys over
HTTP is like sending passwords in plain text. See :doc:`security` for more details.

``ENABLE_AUDIT_LOGGING``
-------------------------

Controls whether security events are logged. When enabled, the package logs
authentication attempts, API key creation/revocation, and security-related events.

**Default:** ``True``

**Example:**

.. code-block:: python

   DRF_API_KEY = {
       "ENABLE_AUDIT_LOGGING": True,  # Log security events
   }

See :doc:`security` for information about what events are logged and how to access them.

``MAX_ENDPOINTS_PER_KEY``
--------------------------

Limits the number of unique endpoints that can be tracked per API key in analytics.
This helps prevent abuse and keeps your database size manageable.

**Default:** ``1000``

**Example:**

.. code-block:: python

   DRF_API_KEY = {
       "MAX_ENDPOINTS_PER_KEY": 1000,  # Limit tracked endpoints
   }

``MAX_ENDPOINT_LENGTH``
------------------------

Limits the maximum length of endpoint paths stored in analytics. This prevents
malicious or malformed endpoint paths from causing issues.

**Default:** ``500``

**Example:**

.. code-block:: python

   DRF_API_KEY = {
       "MAX_ENDPOINT_LENGTH": 500,  # Maximum endpoint path length
   }

