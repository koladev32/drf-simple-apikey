# Django REST Framework Simple API Key 🔐

Django REST Framework Simple API Key is a simple and fast API Key authentication plugin for REST API built with [Django Rest Framework](https://www.django-rest-framework.org/).

<div>
  <a href="https://badge.fury.io/py/djangorestframework-simple-apikey">
      <img src="https://badge.fury.io/py/djangorestframework-simple-apikey.svg" alt="Version"/>
  </a>
  <a href="https://github.com/koladev32/djangorestframework-simple-apikey/actions/workflows/ci-cd.yml">
      <img src="https://github.com/koladev32/djangorestframework-simple-apikey/actions/workflows/ci-cd.yml/badge.svg" alt="Testing"/>
  </a>
</div>

For the full documentation, visit [https://djangorestframework-simple-apikey.readthedocs.io/en/latest/](https://djangorestframework-simple-apikey.readthedocs.io/en/latest/).

## Introduction

Django REST Simple Api Key is a package built upon Django, Django REST Framework, and the fernet cryptography module to generate, encrypt, and decrypt API keys.

Why should you use this package for your API Key authentication?

* ⚡**️Fast**: We use the [fernet](https://cryptography.io/en/latest/fernet/) cryptography module to generate, encrypt, and decrypt API keys. Besides the security facade, it is blazing fast allowing you to treat requests quickly and easily.
    
* 🔐 **Secure**: Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key, which we call `FERNET_KEY`. As long as you treat the fernet key used to encrypt and decrypt your users API Keys at the same level you treat the Django `SECRET_KEY`, you are good to go.
    
* 🔧 **Customizable**: The models, the authentication backend, and the permissions classes can be rewritten and fit your needs. We do our best to extend Django classes and methods, so you can easily extend our classes and methods.😉 We also provide `SIMPLE_API_KEY` setting you can modify in the `settings.py` file of your Django project.
    

## Quickstart

Install with `pip`:

```bash
pip install djangorestframework-simple-apikey
```

You will need to register the application in the `INSTALLED_APPS` in the `settings.py` file of the Django project:

```python
# settings.py

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "rest_framework_simple_api_key",
]
```

And you will also need to have a setting called `FERNET_KEY`. You can generate a fernet key using the `python manage.py generate_fernet_key` command.

```python
SIMPLE_API_KEY = {
    "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA="
}
```

Run the included migrations:

```bash
python manage.py migrate
```

In your view then, you can add the authentication class and the permission class.

> ⚠️ **Important Note**: By default, the Django user class is used for authentication. You can configure the model you want to use as an entity using `AUTHENTICATION_MODEL` in the `SIMPLE_API_KEY` setting.

```python
from rest_framework import viewsets

from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework.response import Response

class FruitViewSets(viewsets.ViewSet):
    http_method_names = ["get"]
    authentication_classes = (APIKeyAuthentication, )

    def list(self, request):
        return Response([{"detail": True}], 200 )
```

## Generate a Fernet Key
We've made it easier for you by creating a custom Django command to quickly generate a fernet key, which is a **crucial component** in the authentication system. Make sure to keep the key secure and store it somewhere safely (ie: environment variable). 

**Important ⛔️** : You should treat the `FERNET_KEY` security at the same level as the Django `SECRET_KEY`. 🫡

To generate the fernet key use the following command:

```python
python manage.py generate_fernet_key
```
or 

```python
django-admin generate_fernet_key
```

## Changelog

See [CHANGELOG.md](https://github.com/koladev32/djangorestframework-simple-apikey/blob/main/CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](https://github.com/koladev32/djangorestframework-simple-apikey/blob/main/CONTRIBUTING.md).