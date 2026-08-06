Authentification
================

L'authentification est utilisée ici pour identifier une entité et faciliter la vérification de l'autorisation et des permissions pour chaque requête. Par défaut, nous fournissons un backend d'authentification qui vérifie le format de la clé API et s'assure qu'une entité avec cette clé API existe. Django REST Framework est livré avec des backends d'authentification qui définissent le ``request.user``. Avec la classe ``APIKeyAuthentication``, vous pouvez également trouver l'entité de la clé API dans ``request.user``.

   ⚠️ **Note** : Travailler avec ``request.user`` qui n'est pas nécessairement un ``User`` peut être un peu contre-intuitif, mais nous cherchons des solutions pour avoir quelque chose comme ``request.entity`` sans perturber le flux d'authentification et d'autorisation de Django REST Framework. Si vous avez des idées, n'hésitez pas à ouvrir un ticket sur https://github.com/koladev32/drf-simple-apikey/issues.

Utiliser le backend ``APIKeyAuthentication``
--------------------------------------------

Dans votre vue, vous pouvez ajouter la classe ``APIKeyAuthentication`` à l'attribut ``authentication_classes``.

.. code:: python

   class YourViewSet(viewsets.ViewSet):
       http_method_names = ["get"]
       authentication_classes = (APIKeyAuthentication, )
   ...

Par défaut, nous vérifions l'en-tête ``authorization`` pour une valeur avec un format similaire 👉 ``Api-Key VALEUR_DE_LA_CLÉ_API``.

``Api-Key`` est par défaut ``AUTHENTICATION_KEYWORD_HEADER`` que vous pouvez modifier dans le fichier ``settings.py`` de votre projet Django.

.. code:: python

   DRF_API_KEY = {
       ...
       "AUTHENTICATION_KEYWORD_HEADER": "VOTRE_VALEUR_PERSONNALISÉE",
   }

Fonctionnalités de sécurité
---------------------------

Le backend d'authentification inclut plusieurs fonctionnalités de sécurité pour protéger votre API :

- **Protection contre les attaques temporelles** : Nous utilisons des comparaisons à temps constant pour empêcher les attaquants de découvrir des clés API valides en mesurant les temps de réponse.

- **Application de HTTPS** : Par défaut, nous rejetons l'authentification par clé API sur les connexions HTTP non chiffrées en production.

- **Validation des adresses IP** : Lors de l'utilisation de listes blanches ou noires d'IP, nous extrayons et validons les adresses IP en toute sécurité, même derrière des proxys.

Pour plus de détails sur ces fonctionnalités de sécurité et leur fonctionnement, consultez la documentation :doc:`security`.

N'hésitez pas à lire le code de la classe d'authentification sur https://github.com/koladev32/drf-simple-apikey/blob/main/drf-simple-apikey/backends.py.