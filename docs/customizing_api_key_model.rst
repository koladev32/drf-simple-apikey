Customize the APIKey model
===========

You can customize the Api Key model to suit your needs if, for example,
you have an entity different than the default one used. Here’s an
example using a custom class called ``Organization``.

.. code:: python

   # organizations/models.py
   from django.db import models
   from drf-simple-apikey.models import AbstractAPIKey

   class Organization(models.Model):
       name = models.CharField(max_length=255)
       created = models.DateTimeField(auto_now_add=True)

   class OrganizationAPIKey(AbstractAPIKey):
       entity = models.ForeignKey(
           Organization,
           on_delete=models.CASCADE,
           related_name="api_keys",
       )

After that, run the ``makemigrations`` command to generate to tell
Django to generate a new table for the custom model.

.. code:: bash

   python manage.py makemigrations

And then run the migrations.

.. code:: bash

   python manage.py migrate