Personnaliser le modèle APIKey
==============================

Vous pouvez personnaliser le modèle de clé API pour répondre à vos besoins si, par exemple, vous avez une entité différente de celle utilisée par défaut. Voici un exemple utilisant une classe personnalisée appelée ``Organization``.

.. code:: python

   # organizations/models.py
   from django.db import models
   from drf_simple_apikey.models import AbstractAPIKey

   class Organization(models.Model):
       name = models.CharField(max_length=255)
       created = models.DateTimeField(auto_now_add=True)

   class OrganizationAPIKey(AbstractAPIKey):
       entity = models.ForeignKey(
           Organization,
           on_delete=models.CASCADE,
           related_name="api_keys",
       )

Après cela, exécutez la commande ``makemigrations`` pour indiquer à Django de générer une nouvelle table pour le modèle personnalisé.

.. code:: bash

   python manage.py makemigrations

Ensuite, exécutez les migrations.

.. code:: bash

   python manage.py migrate