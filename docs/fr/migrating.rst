Guide de migration pour le renommage du package
================================================

Dans le cadre de nos efforts pour rationaliser nos offres de packages, le package ``djangorestframework-simple-apikey`` a été renommé en ``drf-simple-apikey``. Cette section fournit un guide détaillé sur la façon de migrer votre projet pour utiliser le nouveau nom du package.

Renommage du package
--------------------

1. **Désinstallez l'ancien package** :
   Supprimez le package existant en exécutant la commande suivante dans votre terminal :

   .. code-block:: bash

      pip uninstall djangorestframework-simple-apikey

2. **Installez le nouveau package** :
   Installez le nouveau package en utilisant pip :

   .. code-block:: bash

      pip install drf-simple-apikey

Mise à jour des imports du projet
---------------------------------

Vous devrez mettre à jour vos instructions d'importation dans votre projet Django. Remplacez toutes les instructions d'importation existantes de :

.. code-block:: python

   import djangorestframework_simple_apikey

vers :

.. code-block:: python

   import drf_simple_apikey

Migration des paramètres Django
-------------------------------

Mettez à jour les paramètres de votre projet Django pour refléter les changements dans la configuration du package :

- Remplacez toutes les références des paramètres ``SIMPLE_API_KEY`` par ``DRF_API_KEY``. Par exemple :

  .. code-block:: python

     # Anciens paramètres
     SIMPLE_API_KEY = {
         'API_KEY': 'votre-clé-api-ici',
         'AUTRES_PARAMÈTRES': 'valeurs'
     }

     # Nouveaux paramètres
     DRF_API_KEY = {
         'API_KEY': 'votre-clé-api-ici',
         'AUTRES_PARAMÈTRES': 'valeurs'
     }

Assurez-vous de mettre à jour ces paramètres dans tous les fichiers de configuration de votre projet pour éviter tout problème lors du déploiement ou du développement.

Support et commentaires
-----------------------

Pour plus d'informations, un support détaillé ou pour fournir des commentaires sur le processus de migration, veuillez visiter notre site de documentation à l'adresse https://djangorestframework-simple-apikey.readthedocs.io/en/latest/ ou ouvrir un ticket sur GitHub.

Nous apprécions votre coopération et votre compréhension alors que nous continuons à améliorer nos offres logicielles.