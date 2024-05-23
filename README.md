# Django REST Framework Simple API Key 🔐

Django REST Framework Simple API Key is a fast and secure API Key authentication plugin for REST API built with [Django Rest Framework](https://www.django-rest-framework.org/).

<div>
  <a href="https://badge.fury.io/py/drf-simple-apikey">
      <img src="https://badge.fury.io/py/drf-simple-apikey.svg" alt="Version"/>
  </a>
  <a href="https://github.com/koladev32/drf-simple-apikey/actions/workflows/ci-cd.yml">
      <img src="https://github.com/koladev32/drf-simple-apikey/actions/workflows/ci-cd.yml/badge.svg" alt="Testing"/>
  </a>
</div>

For the full documentation, visit [https://djangorestframework-simple-apikey.readthedocs.io/en/latest/](https://djangorestframework-simple-apikey.readthedocs.io/en/latest/).

## Package Renaming Notice

**Notice:** The `djangorestframework-simple-apikey` package is being renamed to `drf-simple-apikey` to improve usability and align with common naming conventions. Please update your installations:

1. Replace the old package:
   ```bash
   pip uninstall djangorestframework-simple-apikey
   pip install drf-simple-apikey
For the full documentation, visit [https://djangorestframework-simple-apikey.readthedocs.io/en/latest/](https://djangorestframework-simple-apikey.readthedocs.io/en/latest/).

## Introduction

Django REST Simple Api Key is a package built upon Django, Django REST Framework, and the fernet cryptography module to generate, encrypt, and decrypt API keys. It provides fast, secure and customizable API Key authentication.

### Benefits

Why should you use this package for your API Key authentication?

* ⚡**️Fast**: We use the [fernet](https://cryptography.io/en/latest/fernet/) cryptography module to generate, encrypt, and decrypt API keys. Besides the security facade, it is blazing fast allowing you to treat requests quickly and easily.
    
* 🔐 **Secure**: Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key, which we call `FERNET_KEY`. As long as you treat the fernet key at the same level you treat the Django `SECRET_KEY` setting, you are good to go.
    
* 🔧 **Customizable**: The models, authentication backend, and permissions classes can be rewritten and fit your needs. We do our best to extend Django classes and methods, so you can easily extend our classes and methods.😉 Your Api Key authentication settings are kept in a single configuration dictionary named `DRF_API_KEY` in the `settings.py` file of your Django project. It can be customized to fit your project needs.
    

## Quickstart

1 - Install with `pip`:

```bash
pip install drf-simple-apikey
```

2 - Register the app in the `INSTALLED_APPS` in the `settings.py` file:

```python
# settings.py

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "drf_simple_apikey",
]
```

3- Add the `FERNET_KEY` setting in your `DRF_API_KEY` configuration dictionary. You can easily generate a fernet key using the `python manage.py generate_fernet_key` command. Keep in mind that the fernet key plays a huge role in the api key authentication system.

```python
DRF_API_KEY = {
    "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA="
}
```

4 - Run migrations:

```bash
python manage.py migrate
```

In your view then, you can add the authentication class and the permission class.

> ⚠️ **Important Note**: By default, authentication is performed using the `AUTH_USER_MODEL` specified in the settings.py file.

```python
from rest_framework import viewsets

from drf_simple_apikey.backends import APIKeyAuthentication
from rest_framework.response import Response


class FruitViewSets(viewsets.ViewSet):
  http_method_names = ["get"]
  authentication_classes = (APIKeyAuthentication,)

  def list(self, request):
    return Response([{"detail": True}], 200)
```

## Generate a Fernet Key
We've made it easier for you by creating a custom Django command to quickly generate a fernet key, which is a **crucial component** in the authentication system. Make sure to keep the key secure and store it somewhere safely (ie: environment variable). 

**Important ⛔️** : You should treat the `FERNET_KEY` security at the same level as the Django `SECRET_KEY`. 🫡

To generate the fernet key use the following command:

```python
python manage.py generate_fernet_key
```

## Rotation

We implement an API key rotation strategy for this package. To learn more about it, refer to the documentation at https://djangorestframework-simple-apikey.readthedocs.io/en/latest/rotation.html.

## Demo

You can find a demo in project in the `example` directory. To run the project, you can :

```shell
cd example
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Changelog

See [CHANGELOG.md](https://github.com/koladev32/drf-simple-apikey/blob/main/CHANGELOG.md).

## Contributing

Thank you for your interest in contributing to the project! Here's a guide to help you get started:

- **Setup Development Environment:**  
  ```bash
  git clone https://github.com/koladev32/drf-simple-apikey.git
  ```  
  Use the command below to set up your environment:
  ```
  make install
  ```

- **Format the Code:**  
  Before submitting any code, please ensure it is formatted according to our standards:
  ```
  make format
  ```

- **Check Code and Migrations:**  
  Validate your changes against our checks:
  ```
  make check
  ```

- **Run Migrations:**  
  If your changes include database migrations, run the following:
  ```
  make migrations
  ```

- **Run Tests:**  
  Always make sure your changes pass all our tests:
  ```
  make test
  ```

See [CONTRIBUTING.md](https://github.com/koladev32/drf-simple-apikey/blob/main/CONTRIBUTING.md).