Sécurité
========

Garder vos clés API sécurisées est crucial, et nous avons intégré plusieurs fonctionnalités de sécurité dans le package pour aider à protéger votre API. Cette page explique comment ces fonctionnalités fonctionnent et pourquoi elles sont importantes.

Pourquoi la sécurité est importante
-----------------------------------

Les clés API sont comme des mots de passe — si quelqu'un les obtient, il peut accéder à votre API comme s'il était l'utilisateur légitime. C'est pourquoi nous avons implémenté plusieurs couches de sécurité pour protéger vos clés API contre les attaques courantes.

Fonctionnalités de sécurité
---------------------------

Protection contre les attaques temporelles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous êtes-vous déjà demandé si un attaquant pourrait découvrir une clé API valide simplement en mesurant le temps que met votre serveur à répondre ? C'est ce qu'on appelle une attaque temporelle (timing attack), et c'est une réelle préoccupation de sécurité.

**Ce que nous faisons :** Nous utilisons des comparaisons à temps constant et ajoutons de petits délais pour garantir que les tentatives d'authentification échouées prennent le même temps, que le format de la clé API soit valide ou non. Cela signifie que les attaquants ne peuvent rien apprendre d'utile en chronométrant vos réponses.

**Pourquoi c'est important :** Sans cette protection, un attaquant pourrait potentiellement découvrir des clés API valides en mesurant les temps de réponse. Avec elle, il n'obtient aucune information utile des attaques temporelles.

**Comment cela fonctionne :** Le backend d'authentification utilise des fonctions de comparaison sécurisées qui prennent le même temps que la comparaison réussisse ou échoue. Nous ajoutons également un petit délai constant pour normaliser les temps de réponse.

Sécurité de la clé Fernet
~~~~~~~~~~~~~~~~~~~~~~~~~~

Votre clé Fernet est la clé maîtresse qui chiffre et déchiffre toutes vos clés API. Si quelqu'un obtient cette clé, il peut déchiffrer n'importe quelle clé API que vous avez émise. C'est pourquoi nous validons et vérifions votre configuration de clé Fernet.

**Ce que nous vérifions :**
- Le format de la clé est correct (base64, longueur appropriée)
- La clé n'est pas codée en dur dans votre code source (nous vous avertissons si cela semble être le cas)
- La clé suit les meilleures pratiques de sécurité

**Pourquoi c'est important :** Une clé Fernet faible ou exposée compromet toutes vos clés API. Nous aidons à détecter les erreurs courantes avant qu'elles ne deviennent des problèmes de sécurité.

**Bonne pratique :** Stockez toujours votre clé Fernet dans des variables d'environnement, jamais dans votre code source. Traitez-la avec le même soin que votre ``SECRET_KEY`` Django.

Application de HTTPS
~~~~~~~~~~~~~~~~~~~~

Envoyer des clés API via des connexions HTTP non chiffrées, c'est comme écrire votre mot de passe sur une carte postale — toute personne qui intercepte le trafic peut le lire.

**Ce que nous faisons :** Par défaut, nous imposons les connexions HTTPS en production. Si quelqu'un essaie d'utiliser une clé API via HTTP, la requête est rejetée avec un message d'erreur clair.

**Pourquoi c'est important :** Les clés API transmises via HTTP peuvent être interceptées par n'importe qui sur le réseau. HTTPS chiffre la connexion, rendant beaucoup plus difficile le vol de vos clés par les attaquants.

**Comment configurer :** Par défaut, l'application de HTTPS suit automatiquement votre paramètre ``DEBUG``. Quand ``DEBUG=True`` (développement), HTTP est autorisé. Quand ``DEBUG=False`` (production), HTTPS est imposé.

Vous pouvez également le définir explicitement :

.. code-block:: python

   DRF_API_KEY = {
       "ENFORCE_HTTPS": True,  # Active explicitement (ou None pour auto-détection via DEBUG)
   }

**Note :** Le comportement par défaut (``None``) signifie que HTTPS est imposé en production (``DEBUG=False``) et autorisé en développement (``DEBUG=True``). Ainsi, vous n'avez pas à vous en soucier en développement, mais votre API de production reste sécurisée ! 🛡️

Validation des adresses IP
~~~~~~~~~~~~~~~~~~~~~~~~~~

Parfois, vous souhaitez restreindre l'accès par clé API à des adresses IP spécifiques. Mais si vous êtes derrière un proxy ou un équilibreur de charge, les adresses IP peuvent être usurpées si elles ne sont pas traitées correctement.

**Ce que nous faisons :** Nous extrayons en toute sécurité l'adresse IP réelle du client, même lorsque vous êtes derrière des proxys ou des équilibreurs de charge. Nous validons le format IP et gérons en toute sécurité les en-têtes de proxy courants comme ``X-Forwarded-For`` et ``X-Real-IP``.

**Pourquoi c'est important :** Si la validation IP n'est pas effectuée correctement, les attaquants pourraient usurper leur adresse IP en manipulant les en-têtes de proxy. Nous gérons cela en toute sécurité pour que vous n'ayez pas à vous en soucier.

**Comment cela fonctionne :** Le backend d'authentification vérifie l'adresse IP à partir de sources fiables, valide le format, et revient à ``REMOTE_ADDR`` si les en-têtes de proxy ne sont pas disponibles ou fiables.

Assainissement des entrées
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors du suivi de l'utilisation de l'API dans l'analytique, nous stockons quels points de terminaison ont été accédés. Mais que faire si quelqu'un essaie d'envoyer des données malveillantes dans le chemin du point de terminaison ?

**Ce que nous faisons :** Nous assainissons et validons les chemins des points de terminaison avant de les stocker. Nous supprimons les caractères dangereux, limitons la longueur et plafonnons le nombre de points de terminaison uniques suivis par clé API.

**Pourquoi c'est important :** Sans assainissement, des chemins de points de terminaison malveillants ou mal formés pourraient causer des problèmes dans votre base de données ou votre analytique. Nous les nettoyons automatiquement.

**Comment configurer :** Vous pouvez définir des limites dans vos paramètres :

.. code-block:: python

   DRF_API_KEY = {
       "MAX_ENDPOINTS_PER_KEY": 1000,  # Nombre maximum de points de terminaison uniques à suivre
       "MAX_ENDPOINT_LENGTH": 500,     # Longueur maximale du chemin du point de terminaison
   }

Journalisation d'audit
~~~~~~~~~~~~~~~~~~~~~~

Savoir qui a accédé à quoi et quand est crucial pour la sécurité. C'est pourquoi nous enregistrons les événements de sécurité importants.

**Ce que nous enregistrons :**
- Tentatives d'authentification réussies et échouées
- Création et révocation de clés API
- Refus d'accès basés sur l'IP
- Erreurs liées à la sécurité

**Pourquoi c'est important :** Si quelque chose tourne mal, les journaux d'audit vous aident à comprendre ce qui s'est passé. Vous pouvez voir qui a accédé à votre API, quand et d'où.

**Comment y accéder :** Les journaux d'audit sont écrits dans le système de journalisation de Django. Configurez vos paramètres de journalisation pour capturer ces événements :

.. code-block:: python

   LOGGING = {
       'version': 1,
       'handlers': {
           'file': {
               'class': 'logging.FileHandler',
               'filename': 'security.log',
           },
       },
       'loggers': {
           'drf_simple_apikey': {
               'handlers': ['file'],
               'level': 'INFO',
           },
       },
   }

Bonnes pratiques de sécurité
----------------------------

Voici quelques recommandations pour garder vos clés API sécurisées :

1. **Stockez les clés Fernet en toute sécurité** : Utilisez toujours des variables d'environnement, ne les codez jamais en dur dans votre code source. Utilisez un service de gestion des secrets en production.

2. **Utilisez HTTPS** : Imposez toujours HTTPS en production. N'envoyez jamais de clés API via des connexions non chiffrées.

3. **Faites pivoter les clés régulièrement** : Utilisez la fonctionnalité de rotation pour changer périodiquement vos clés de chiffrement. Voir :doc:`rotation` pour plus de détails.

4. **Surveillez les journaux d'audit** : Examinez régulièrement vos journaux d'audit pour détecter des activités suspectes. Recherchez des schémas inhabituels ou des tentatives d'authentification répétées échouées.

5. **Limitez l'accès IP** : Lorsque c'est possible, utilisez une liste blanche d'IP pour restreindre l'accès par clé API à des adresses IP connues.

6. **Révoquez les clés compromises** : Si vous soupçonnez qu'une clé API a été compromise, révoquez-la immédiatement via l'interface d'administration ou par programmation.

7. **Maintenez les dépendances à jour** : Mettez régulièrement à jour le package et ses dépendances pour obtenir les derniers correctifs de sécurité.