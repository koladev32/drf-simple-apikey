Paramètres
===========

Certains comportements de Django REST Framework Simple API Key peuvent être personnalisés via des variables de configuration dans ``settings.py``. Vous trouverez ci-dessous la configuration par défaut de `DRF_API_KEY`.

.. code-block:: python

  # settings.py du projet Django
  ...

  DRF_API_KEY = {
       "FERNET_SECRET": "",
       "API_KEY_LIFETIME": 365,
       "AUTHENTICATION_KEYWORD_HEADER": "Api-Key",
       "ROTATION_PERIOD": timedelta(days=7),
       "ROTATION_FERNET_SECRET": "",
       "IGNORED_ROUTES": ["/admin/"]  # Routes qui doivent être ignorées par l'authentification par clé API
  }
Ci-dessus, les valeurs par défaut de ces paramètres sont affichées.

``FERNET_SECRET``
-------------------------
La clé fernet (`Fernet <https://cryptography.io/en/latest/fernet/>`__) est utilisée pour chiffrer et déchiffrer les clés API.

Pour générer une nouvelle clé fernet, vous pouvez utiliser la commande suivante :

 python manage.py generate_fernet_key

Assurez-vous de la stocker dans un endroit sûr et de la traiter comme vous traiteriez la configuration ``SECRET_KEY`` de Django.

``API_KEY_LIFETIME``
--------------------------

Détermine la période de validité d'une clé API générée. La valeur par défaut est 365 jours.

``AUTHENTICATION_KEYWORD_HEADER``
----------------------------

Détermine le mot-clé qui doit accompagner chaque requête effectuée vers votre API. La valeur par défaut est ``Api-Key`` et il est utilisé dans le format suivant :

 Api-Key CLÉ_API

``ROTATION_PERIOD``
-------------------------
La durée pendant laquelle la rotation des clés reste active. Après cette période, le processus de rotation se termine et vous devrez échanger manuellement les valeurs de ``FERNET_SECRET`` et ``ROTATION_FERNET_SECRET``.

**Valeur par défaut :** ``timedelta(days=7)``

**Exemple :**

.. code-block:: python

   from datetime import timedelta

   DRF_API_KEY = {
       "ROTATION_PERIOD": timedelta(days=7),  # Rotation active pendant 7 jours
   }

``ROTATION_FERNET_SECRET``
-------------------------
Le ``ROTATION_FERNET_SECRET`` est une clé Fernet secondaire (`Fernet <https://cryptography.io/en/latest/fernet/>`__) utilisée dans le cadre du système cryptographique ``MultiFernet``.
Alors que la clé Fernet principale (**fernet_key**) est utilisée pour le chiffrement et déchiffrement principal, le ``ROTATION_FERNET_SECRET`` joue un rôle central pendant les phases de rotation des clés.

Dans le contexte de ``MultiFernet`` :

- Les nouveaux jetons sont chiffrés en utilisant le ``ROTATION_FERNET_SECRET``.
- Les jetons peuvent être déchiffrés avec soit le ``ROTATION_FERNET_SECRET``, ce qui permet une rotation fluide des clés sans rendre obsolètes les jetons existants.

.. code-block:: bash

   python manage.py generate_fernet_key

Cette utilisation stratégique garantit que lors de la transition vers une nouvelle clé, les anciens jetons chiffrés avec l'ancienne clé restent valides, et les nouveaux jetons sont chiffrés avec la nouvelle clé.
Ainsi, une transition transparente est réalisée, améliorant la sécurité sans causer de perturbations.

``IGNORED_ROUTES``
-------------------------
Une liste de chemins d'URL qui doivent être ignorés par l'analyseur de clés API (middleware d'analytique). Toute requête vers un chemin commençant par l'une de ces routes ne sera pas tracée dans l'analytique. La valeur par défaut est ``["/admin/"]``. Ce paramètre est spécifiquement utilisé par le middleware d'analytique pour déterminer quelles routes doivent être exclues du suivi d'utilisation.

Exemple :
.. code-block:: python

  DRF_API_KEY = {
      "IGNORED_ROUTES": [
          "/admin/",  # Exclut les routes d'administration de l'analytique
          "/api/documents/",  # Exclut les routes API de documents de l'analytique
          "/health/",  # Exclut les points de contrôle de santé de l'analytique
      ]
  }

``ENFORCE_HTTPS``
-------------------------

Par défaut, nous imposons les connexions HTTPS en production pour empêcher la transmission des clés API via HTTP non chiffré. Si quelqu'un essaie d'utiliser une clé API via HTTP, la requête sera rejetée.

**Valeur par défaut :** ``None`` (détection automatique : ``True`` quand ``DEBUG=False``, ``False`` quand ``DEBUG=True``)

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "ENFORCE_HTTPS": True,  # Rejette les requêtes HTTP en production
   }

**Note :** ⚠️ Définissez toujours ce paramètre sur ``True`` en production ! Envoyer des clés API via HTTP équivaut à envoyer des mots de passe en texte clair. Voir :doc:`security` pour plus de détails.

``ENABLE_AUDIT_LOGGING``
-------------------------

Contrôle si les événements de sécurité sont enregistrés. Lorsqu'il est activé, le package enregistre les tentatives d'authentification, la création/révocation de clés API et les événements liés à la sécurité.

**Valeur par défaut :** ``True``

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "ENABLE_AUDIT_LOGGING": True,  # Enregistre les événements de sécurité
   }

Voir :doc:`security` pour plus d'informations sur les événements enregistrés et comment y accéder.

``MAX_ENDPOINTS_PER_KEY``
--------------------------

Limite le nombre de points de terminaison uniques pouvant être suivis par clé API dans l'analytique. Cela aide à prévenir les abus et à maintenir une taille de base de données gérable.

**Valeur par défaut :** ``1000``

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "MAX_ENDPOINTS_PER_KEY": 1000,  # Limite les points de terminaison suivis
   }

``MAX_ENDPOINT_LENGTH``
------------------------

Limite la longueur maximale des chemins de points de terminaison stockés dans l'analytique. Cela empêche les chemins de points de terminaison malveillants ou mal formés de causer des problèmes.

**Valeur par défaut :** ``500``

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "MAX_ENDPOINT_LENGTH": 500,  # Longueur maximale du chemin du point de terminaison
   }

``IP_ADDRESS_HEADER``
------------------------

Spécifie quel en-tête HTTP utiliser pour extraire l'adresse IP du client. Ceci est utile lorsque votre application se trouve derrière un proxy ou un équilibreur de charge.

**Valeur par défaut :** ``"REMOTE_ADDR"``

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "IP_ADDRESS_HEADER": "HTTP_X_FORWARDED_FOR",  # Utilise l'en-tête X-Forwarded-For
   }

**Note :** Le backend d'authentification gère en toute sécurité les en-têtes de proxy pour éviter l'usurpation d'IP. Voir :doc:`security` pour plus de détails.

``API_KEY_CLASS``
------------------------

Le chemin complet qualifié vers votre classe de modèle de clé API personnalisée, si vous en avez créé une. Ceci est utilisé par l'addon d'analytique pour référencer le modèle de clé API.

**Valeur par défaut :** ``"drf_simple_apikey.Apikey"``

**Exemple :**

.. code-block:: python

   DRF_API_KEY = {
       "API_KEY_CLASS": "myapp.models.CustomAPIKey",  # Utilise un modèle personnalisé
   }

**Note :** Modifiez ceci uniquement si vous avez créé un modèle de clé API personnalisé. Voir :doc:`customizing_api_key_model` pour plus de détails.