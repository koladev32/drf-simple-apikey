"""
Django REST framework Simple API Key Configurations
"""

import django

import warnings

warnings.warn(
    "This package, 'djangorestframework-simple-apikey', has been renamed to 'drf-apikey' and will no longer be updated."
    "Please switch to the new package to continue receiving updates and support. "
    "For more information and migration instructions, please visit: https://drf-apikey.readthedocs.io/en/latest/migrating.html",
    DeprecationWarning,
    stacklevel=2,
)


__title__ = "Django REST framework Simple API Key"
__author__ = ["Kolawole Mangabo", "Ruben Atinho"]


# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = "iso-8859-1"
