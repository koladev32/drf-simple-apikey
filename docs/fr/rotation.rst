Rotation des clés API
=====================

La rotation des clés API est un mécanisme de sécurité conçu pour renforcer la sécurité de votre API en changeant périodiquement les clés cryptographiques utilisées pour chiffrer et déchiffrer les clés API. Ce processus implique une transition transparente d'une ancienne clé vers une nouvelle, garantissant une perturbation minimale pour les consommateurs de votre API tout en augmentant la sécurité.

Ce document explique comment activer et configurer la rotation des clés API dans votre projet Django en utilisant le package, détaillant le fonctionnement interne du processus de rotation.

Aperçu de la rotation des clés
------------------------------

La rotation des clés API dans le package `drf-simple-apikey` implique de changer périodiquement les clés de chiffrement utilisées pour sécuriser les clés API. Pendant la rotation, une nouvelle clé est introduite, et les clés anciennes et nouvelles sont utilisées pendant une période de transition. Cela garantit que les clés API existantes restent valides tandis que les nouvelles clés sont chiffrées avec la nouvelle clé.

Activation
----------

Avant d'activer une rotation, assurez-vous de définir la clé Fernet de rotation ``ROTATION_FERNET_SECRET`` dans les paramètres du package.

Vous devrez ajouter l'application de rotation ``drf_simple_apikey.rotation`` dans le paramètre Django ``INSTALLED_APPS`` de votre projet.

   .. code-block:: python

       INSTALLED_APPS = (
            ...
            "rest_framework",
            "drf_simple_apikey",
            "drf_simple_apikey.rotation",  # Application ajoutée
        )

Et vous devrez exécuter la commande de migration :

   .. code-block:: shell

      python manage.py migrate drf-simple-apikey_rotation

Pour activer la rotation des clés API, vous pouvez choisir l'une des méthodes suivantes :

Utilisation de la commande de gestion Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ouvrez votre terminal.

2. Exécutez la commande de gestion Django suivante pour démarrer la rotation des clés :

   .. code-block:: shell

      python manage.py rotation

   Cette commande initialise le processus de rotation, créant un objet de rotation et définissant le drapeau `is_rotation_enabled` à `True` dans la base de données.

3. Pour arrêter la rotation, exécutez la commande suivante :

   .. code-block:: shell

      python manage.py rotation --stop

   Cette commande désactive le processus de rotation en définissant le drapeau `is_rotation_enabled` à `False` pour le dernier objet de rotation avec `is_rotation_enabled` à `False`.

Utilisation de l'interface d'administration Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Accédez à votre interface d'administration Django.

2. Naviguez jusqu'à la section "Rotation des clés API".

3. Pour activer la rotation, créez une nouvelle entrée de rotation en cliquant sur le bouton "Ajouter" pour créer un nouvel objet de rotation.

4. Pour désactiver la rotation, modifiez l'entrée de rotation et définissez le drapeau `is_rotation_enabled` à `False`.

Comment fonctionne la rotation
------------------------------

La rotation des clés API opère à travers plusieurs phases clés pour garantir une transition fluide tout en maintenant la sécurité de vos clés API.

Phases de la rotation des clés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Phase d'initialisation** : La rotation commence lorsque vous l'activez en utilisant les méthodes mentionnées ci-dessus.

2. **Phase de transition** : Pendant cette phase, les clés anciennes et nouvelles sont actives. Les clés API existantes continuent de fonctionner, et les nouvelles clés sont chiffrées en utilisant la nouvelle clé.

3. **Phase d'achèvement** : Après une période définie (``ROTATION_PERIOD``), l'ancienne clé n'est plus utilisée. Les nouvelles clés API sont chiffrées exclusivement avec la nouvelle clé. À cet effet, vous devrez échanger manuellement les valeurs de ``ROTATION_FERNET_SECRET`` et ``FERNET_SECRET``.

Utilisation des clés pendant la rotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Déchiffrement** : Les clés API peuvent être déchiffrées en utilisant soit l'ancienne, soit la nouvelle clé pendant la phase de transition, garantissant que les clés existantes restent valides.

- **Chiffrement** : Pendant la rotation, les nouvelles clés API sont chiffrées en utilisant la nouvelle clé pour garantir une sécurité renforcée.