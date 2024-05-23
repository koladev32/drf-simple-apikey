Authentication
===========

Authentication is used here to identify an entity and make it easy to
verify authorization and permissions on each request. By default, we
provide an authentication backend that checks for the API Key format and
ensures that an entity with this API key exists. Django REST Framework
comes with authentication backends that set the ``request.user``. With
the ``APIKeyAuthentication`` class, you can find the entity of the Api
Key at ``request.user`` too.

   Working with `request.user` which might not necessarily be an `User` might be a little bit counter-intuitive, but we are looking for
   solutions to have something such as ``request.entity`` without having
   to disrupt the Django REST Framework authentication and authorization
   flow. If you have some ideas, feel free to open an issue
   https://github.com/koladev32/drf-simple-apikey/issues.

Use the ``APIKeyAuthentication`` backend
----------------------------------------

In your view, you can add the ``APIKeyAuthentication`` class to the
``authentication_classes`` attribute.

.. code:: python

   class YourViewSet(viewsets.ViewSet):
       http_method_names = ["get"]
       authentication_classes = (APIKeyAuthentication, )
   ...

By default, we check the ``authorization`` header for a value with a
similar format 👉 ``Api-Key API_KEY_VALUE``.

The ``Api-Key`` is by default ``AUTHENTICATION_KEYWORD_HEADER`` which
you can modify in the ``settings.py`` file of your Django project.

.. code:: python

   DRF_API_KEY = {
       ...
       "AUTHENTICATION_KEYWORD_HEADER": "YOUR_CUSTOM_VALUE",
   }

Feel free to read the code of the authentication class at
https://github.com/koladev32/drf-simple-apikey/blob/main/drf-simple-apikey/backends.py.
