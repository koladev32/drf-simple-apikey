Getting Started
==============

Django REST Framework Simple API Key is fast and secure API Key
authentication plugin for REST API built with `Django Rest
Framework <https://www.django-rest-framework.org/>`__.

.. container::

Introduction
------------

Django REST Simple Api Key is a package built upon Django, Django REST
Framework, and the fernet cryptography module to generate, encrypt, and
decrypt API keys. It provides fast, secure and customizable API Key
authentication.

Benefits
~~~~~~~~

Why should you use this package for your API Key authentication?

-  ⚡\ **️Fast**: We use the
   `fernet <https://cryptography.io/en/latest/fernet/>`__ cryptography
   module to generate, encrypt, and decrypt API keys. Besides the
   security facade, it is blazing fast allowing you to treat requests
   quickly and easily.

-  🔐 **Secure**: Fernet guarantees that a message encrypted using it
   cannot be manipulated or read without the key, which we call
   ``FERNET_KEY``. As long as you treat the fernet key at the same level
   you treat the Django ``SECRET_KEY`` setting, you are good to go.

-  🔧 **Customizable**: The models, authentication backend, and
   permissions classes can be rewritten and fit your needs. We do our
   best to extend Django classes and methods, so you can easily extend
   our classes and methods.😉 Your Api Key authentication settings are
   kept in a single configuration dictionary named ``SIMPLE_API_KEY`` in
   the ``settings.py`` file of your Django project. It can be customized
   to fit your project needs.

Quickstart
----------

1 - Install with ``pip``:

.. code:: bash

   pip install drf-apikey

2 - Register the app in the ``INSTALLED_APPS`` in the ``settings.py``
file:

.. code:: python

   # settings.py

   INSTALLED_APPS = [
     # ...
     "rest_framework",
     "drf-apikey",
   ]

3- Add the ``FERNET_KEY`` setting in your ``SIMPLE_API_KEY``
configuration dictionary. You can easily generate a fernet key using the
``python manage.py generate_fernet_key`` command. Keep in mind that the
fernet key plays a huge role in the api key authentication system.

.. code:: python

   SIMPLE_API_KEY = {
       "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA="
   }

4 - Run migrations:

.. code:: bash

   python manage.py migrate

In your view then, you can add the authentication class and the
permission class.

   ⚠️ **Important Note**: By default, the Django User class
   (django.contrib.auth.User) is used for authentication.

.. code:: python

   from rest_framework import viewsets

   from drf-apikey.backends import APIKeyAuthentication
   from rest_framework.response import Response

   class FruitViewSets(viewsets.ViewSet):
       http_method_names = ["get"]
       authentication_classes = (APIKeyAuthentication, )

       def list(self, request):
           return Response([{"detail": True}], 200 )

Generate a Fernet Key
---------------------

We’ve made it easier for you by creating a custom Django command to
quickly generate a fernet key, which is a **crucial component** in the
authentication system. Make sure to keep the key secure and store it
somewhere safely (ie: environment variable).

**Important ⛔️** : You should treat the ``FERNET_KEY`` security at the
same level as the Django ``SECRET_KEY``. 🫡

To generate the fernet key use the following command:

.. code:: bash

   python manage.py generate_fernet_key

Changelog
---------

See
`CHANGELOG.md <https://github.com/koladev32/drf-apikey/blob/main/CHANGELOG.md>`__.

Contributing
------------

See
`CONTRIBUTING.md <https://github.com/koladev32/drf-apikey/blob/main/CONTRIBUTING.md>`__.