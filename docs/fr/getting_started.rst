Pour commencer
==============

Django REST Framework Simple API Key est une extension d'authentification par clé API rapide et sécurisée pour les API REST construites avec `Django REST Framework <https://www.django-rest-framework.org/>`__.

.. container::

Introduction
------------

Django REST Simple API Key est un package construit sur Django, Django REST Framework, et le module de cryptographie fernet pour générer, chiffrer et déchiffrer des clés API. Il fournit une authentification par clé API rapide, sécurisée et personnalisable.

Avantages
~~~~~~~~~

Pourquoi devriez-vous utiliser ce package pour votre authentification par clé API ?

-  ⚡ **Rapide** : Nous utilisons le module de cryptographie
   `fernet <https://cryptography.io/en/latest/fernet/>`__ pour générer, chiffrer et déchiffrer les clés API. En plus de la couche de sécurité, c'est extrêmement rapide, ce qui vous permet de traiter les requêtes rapidement et facilement.

-  🔐 **Sécurisé** : Fernet garantit qu'un message chiffré avec celui-ci ne peut pas être manipulé ou lu sans la clé, que nous appelons ``FERNET_KEY``. Tant que vous traitez la clé fernet au même niveau que la configuration ``SECRET_KEY`` de Django, vous êtes prêt.

-  🔧 **Personnalisable** : Les modèles, le backend d'authentification et les classes de permissions peuvent être réécrits et adaptés à vos besoins. Nous faisons de notre mieux pour étendre les classes et méthodes de Django, afin que vous puissiez facilement étendre nos classes et méthodes. 😉 Vos paramètres d'authentification par clé API sont conservés dans un seul dictionnaire de configuration nommé ``DRF_API_KEY`` dans le fichier ``settings.py`` de votre projet Django. Il peut être personnalisé pour répondre aux besoins de votre projet.

Démarrage rapide
----------------

1 - Installez avec ``pip`` :

.. code:: bash

   pip install drf-simple-apikey

2 - Enregistrez l'application dans ``INSTALLED_APPS`` dans le fichier ``settings.py`` :

.. code:: python

   # settings.py

   INSTALLED_APPS = [
     # ...
     "rest_framework",
     "drf_simple_apikey",
   ]

3 - Ajoutez la configuration ``FERNET_KEY`` dans votre dictionnaire de configuration ``DRF_API_KEY``. Vous pouvez facilement générer une clé fernet en utilisant la commande ``python manage.py generate_fernet_key``. Gardez à l'esprit que la clé fernet joue un rôle crucial dans le système d'authentification par clé API.

.. code:: python

   DRF_API_KEY = {
       "FERNET_SECRET": "sVjomf7FFy351xRxDeJWFJAZaE2tG3MTuUv92TLFfOA="
   }

4 - Exécutez les migrations :

.. code:: bash

   python manage.py migrate

Dans votre vue, vous pouvez ensuite ajouter la classe d'authentification et la classe de permission.

   ⚠️ **Note importante** : Par défaut, la classe User de Django (django.contrib.auth.User) est utilisée pour l'authentification.

.. code:: python

   from rest_framework import viewsets

   from drf_simple_apikey.backends import APIKeyAuthentication
   from rest_framework.response import Response

   class FruitViewSets(viewsets.ViewSet):
       http_method_names = ["get"]
       authentication_classes = (APIKeyAuthentication, )

       def list(self, request):
           return Response([{"detail": True}], 200 )

Générer une clé Fernet
-----------------------

Nous avons facilité les choses en créant une commande Django personnalisée pour générer rapidement une clé fernet, qui est un **composant crucial** du système d'authentification. Assurez-vous de garder la clé sécurisée et de la stocker dans un endroit sûr (par exemple : variable d'environnement).

**Important ⛔️** : Vous devez traiter la sécurité de ``FERNET_KEY`` au même niveau que la ``SECRET_KEY`` de Django. 🫡

Pour générer la clé fernet, utilisez la commande suivante :

.. code:: bash

   python manage.py generate_fernet_key

Considérations de sécurité
---------------------------

Avant de passer en production, voici quelques conseils de sécurité à garder à l'esprit :

- **Traitez votre clé Fernet comme votre SECRET_KEY Django** : Stockez-la dans des variables d'environnement, ne la committez jamais dans le contrôle de version, et faites-la pivoter périodiquement.

- **Utilisez toujours HTTPS en production** : Le package peut imposer des connexions HTTPS pour empêcher la transmission des clés API via HTTP non chiffré. Voir :doc:`security` pour plus de détails.

- **Consultez vos journaux d'audit** : Le package enregistre les événements de sécurité importants. Assurez-vous de surveiller ces journaux pour détecter toute activité suspecte.

Pour plus d'informations détaillées sur la sécurité, consultez la documentation :doc:`security`.

Journal des modifications
-------------------------

Voir
`CHANGELOG.md <https://github.com/koladev32/drf-simple-apikey/blob/main/CHANGELOG.md>`__.

Contribuer
----------

Voir
`CONTRIBUTING.md <https://github.com/koladev32/drf-simple-apikey/blob/main/CONTRIBUTING.md>`__.