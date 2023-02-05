# Django REST Framework Simple API Key

Simple API Key is an API Key authentication plugin for REST API built with [Django Rest Framework](https://www.django-rest-framework.org/).

[![PyPI version](https://badge.fury.io/py/djangorestframework-simple-apikey.svg)](https://badge.fury.io/py/djangorestframework-simple-apikey)

For the full documentation, visit https://djangorestframework-simple-apikey.readthedocs.io/en/latest/.

## Introduction

...

## Quickstart

Install with `pip`:

```bash
pip install djangorestframework-simple-apikey
```

You will need to register the application in the  `INSTALLED_APPS` in `settings.py` file of the Django project:

```python
# settings.py

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "rest_framework_simple_api_key",
]
```

Run the included migrations:

```bash
python manage.py migrate
```

In your views then, you can add the authentication class and the permission class. 

> **Note**⚠️: By default, the Django user class is used for authentication. You can configure the model you want to use as an entity using `AUTHENTICATION_MODEL` in the `SIMPLE_API_KEY` setting.

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

## Changelog

See [CHANGELOG.md](https://github.com/koladev32/djangorestframework-simple-apikey/blob/main/CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](https://github.com/koladev32/djangorestframework-simple-apikey/blob/main/CONTRIBUTING.md).
