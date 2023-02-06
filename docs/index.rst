Django REST Simple Api Key
==========

.. image:: https://badge.fury.io/py/djangorestframework-simple-apikey.svg/
   :target: https://github.com/koladev32/djangorestframework-simple-apikey/

.. image:: https://github.com/koladev32/djangorestframework-simple-apikey/actions/workflows/ci-cd.yml/badge.svg/
   :target: https://github.com/koladev32/djangorestframework-simple-apikey/actions/workflows/ci-cd.yml/

.. image:: https://readthedocs.org/projects/djangorestframework-simple-apikey/badge/?version=latest
    :target: https://djangorestframework-simple-apikey.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

An API Key authentication plugin for the `Django REST Framework
<http://www.django-rest-framework.org/>`__.

-------------------------------------------------------------------------------

Django REST Simple Api Key is a package built upon Django, Django REST Framework, and the fernet cryptography module to generate, encrypt, and decrypt API keys.

Why should you use this package for your API Key authentication?

* ⚡ **Fast**: We use the [fernet](https://cryptography.io/en/latest/fernet/) cryptography module to generate, encrypt, and decrypt API keys. Besides the security facade, it is blazing fast allowing you to treat requests quickly and easily.

* 🔐 **Secure**: Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key, which we call `FERNET_KEY`. As long as you treat the fernet key used to encrypt and decrypt your users API Keys at the same level you treat the Django `SECRET_KEY`, you are good to go.

* 🔧 **Customizable**: The models, the authentication backend, and the permissions classes can be rewritten and fit your needs. We do our best to extend Django classes and methods, so you can easily extend our classes and methods.😉 We also provide `SIMPLE_API_KEY` setting you can modify in the `settings.py` file of your Django project.



Acknowledgments
---------------

This project borrows code from the `Django REST Framework
<https://github.com/encode/django-rest-framework/>`__ as well as concepts from
the implementation of another JSON web token library for the Django REST
Framework, `django-rest-framework-jwt
<https://github.com/GetBlimp/django-rest-framework-jwt>`__.  The licenses from
both of those projects have been included in this repository in the "licenses"
directory.

Contents
--------

.. toctree::
    :maxdepth: 3

    getting_started
    settings
    permissions
    authentication
    token_types
    development_and_contributing
    changelog


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
