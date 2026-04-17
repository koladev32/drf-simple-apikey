Middleware d'analyse des clés API
=================================

Le middleware d'analyse des clés API est un composant du package `drf-simple-apikey` qui fournit des analyses en temps réel sur l'utilisation des clés API. Il enregistre chaque requête API, suivant quels points de terminaison sont accédés et à quelle fréquence.

Cas d'utilisation du middleware d'analyse des clés API
=======================================================

Voici pourquoi vous pouvez utiliser la fonctionnalité d'analyse dans votre application :

- **Prise de décision améliorée** : Il fournit des données complètes sur les schémas d'utilisation de l'API, permettant une meilleure gestion des ressources et des décisions d'optimisation.

- **Facturation précise** : Vous pouvez l'utiliser pour une facturation précise en suivant l'utilisation de l'API par chaque utilisateur, garantissant que les clients sont facturés en fonction de leur utilisation réelle.

- **Surveillance de sécurité améliorée** : Il surveille les schémas d'accès à l'API qui peuvent vous aider à détecter et à répondre rapidement aux activités non autorisées ou suspectes.

Cette page détaille comment intégrer et configurer le middleware d'analyse des clés API dans votre projet Django, et explique son fonctionnement.

Aperçu du middleware
--------------------

Le `ApiKeyAnalyticsMiddleware` suit automatiquement l'accès aux différents points de terminaison de l'API en interceptant les requêtes API. Il enregistre chaque accès dans la base de données, vous permettant de surveiller l'utilisation de l'API et d'optimiser les allocations de clés API.

Configuration
-------------

Pour utiliser le `ApiKeyAnalyticsMiddleware`, suivez ces instructions de configuration :

1. Assurez-vous que l'application du middleware `drf_simple_apikey.analytics` est incluse dans le paramètre ``INSTALLED_APPS`` de votre projet Django.

   .. code-block:: python

       INSTALLED_APPS = (
           ...
           "rest_framework",
           "drf_simple_apikey",
           "drf_simple_apikey.analytics",  # Assurez-vous que cette application est ajoutée
       )

2. Ajoutez le `ApiKeyAnalyticsMiddleware` aux paramètres `MIDDLEWARE` dans votre configuration Django.

   .. code-block:: python

       MIDDLEWARE = [
           ...
           'django.middleware.security.SecurityMiddleware',
           'drf_simple_apikey.analytics.middleware.ApiKeyAnalyticsMiddleware',  # Ajoutez le middleware ici
           ...
       ]

3. Exécutez la commande de migration pour créer les tables de base de données nécessaires :

   .. code-block:: shell

      python manage.py migrate drf-simple-apikey_analytics

Activation
----------

Le middleware est activé dès qu'il est ajouté à la liste `MIDDLEWARE` et que le projet est redémarré. Aucune action supplémentaire n'est nécessaire pour commencer à collecter des données.

Comment fonctionne le middleware
--------------------------------

Une fois activé, le middleware remplit les fonctions suivantes :

1. **Interception des requêtes** : Lors de la réception d'une requête API, le middleware extrait la clé API utilisée pour authentifier la requête.

2. **Suivi des points de terminaison** : Il enregistre le point de terminaison accédé par la clé API.

3. **Stockage des données** : Toutes les données d'accès sont stockées dans le modèle `ApiKeyAnalytics`, qui peut être interrogé pour récupérer des analyses.

Accès aux données
-----------------

Pour accéder aux données d'analyse :

1. Utilisez l'interface d'administration de Django pour visualiser et gérer les données collectées par le middleware.

2. Accédez au modèle `ApiKeyAnalytics` via l'ORM de Django pour effectuer des requêtes personnalisées ou exporter des données pour une analyse plus approfondie.

Sécurité et protection des données
----------------------------------

Nous prenons la sécurité au sérieux, même dans l'analytique. C'est pourquoi nous assainissons automatiquement les chemins des points de terminaison avant de les stocker. Cela empêche les données malveillantes ou mal formées de causer des problèmes dans votre base de données.

**Ce que nous faisons :**
- Nettoyage des chemins des points de terminaison (suppression des caractères dangereux)
- Limitation de la longueur du chemin du point de terminaison
- Plafonnement du nombre de points de terminaison uniques suivis par clé API

**Pourquoi c'est important :** Sans assainissement, quelqu'un pourrait potentiellement envoyer des données malveillantes qui pourraient causer des problèmes dans votre base de données ou vos rapports d'analyse. Nous gérons cela automatiquement, vous n'avez donc pas à vous en soucier.

Vous pouvez configurer ces limites dans vos paramètres — voir :doc:`settings` pour plus de détails. Pour plus d'informations sur les fonctionnalités de sécurité, consultez la documentation :doc:`security`.