Développement et contribution
=============================

Lorsque vous contribuez à ce dépôt, veuillez d'abord discuter du changement que vous souhaitez apporter via un ticket, un e-mail ou toute autre méthode avec les propriétaires de ce dépôt avant d'effectuer un changement.

Veuillez noter que nous avons un code de conduite, veuillez le suivre dans toutes vos interactions avec le projet.

Processus de pull request
-------------------------

1. Assurez-vous de supprimer toutes les dépendances d'installation ou de construction avant la fin de la couche lors d'une construction.
2. Mettez à jour le README.md avec les détails des changements apportés à l'interface, ce qui inclut les nouvelles variables d'environnement, les ports exposés, les emplacements de fichiers utiles et les paramètres des conteneurs.
3. Augmentez les numéros de version dans les fichiers d'exemples et le README.md à la nouvelle version que cette pull request représenterait. Le système de versionnement que nous utilisons est `SemVer <http://semver.org/>`__.
4. Vous pouvez fusionner la pull request une fois que vous avez l'approbation de deux autres développeurs, ou si vous n'avez pas la permission de le faire, vous pouvez demander au deuxième relecteur de la fusionner pour vous.

Gestion des versions
--------------------

Nous utilisons `bump2version <https://github.com/c4urself/bump2version>`__ pour gérer les numéros de version dans l'ensemble du projet. Cela garantit que les numéros de version sont mis à jour de manière cohérente à tous les endroits appropriés.

**Installation de bump2version :**

.. code-block:: bash

   pip install bump2version

**Comment cela fonctionne :**

Le projet utilise un fichier ``setup.cfg`` pour configurer bump2version. Il met automatiquement à jour les numéros de version dans :

- ``setup.cfg`` (current_version)
- ``pyproject.toml`` (champ version)
- ``drf_simple_apikey/version.py`` (constante VERSION)
- ``CHANGELOG.md`` (ajoute une nouvelle entrée de version avec la date)

**Incrémentation des versions :**

Pour incrémenter la version, utilisez l'une de ces commandes :

.. code-block:: bash

   # Incrémentation de version patch (2.2.1 → 2.2.2)
   bump2version patch

   # Incrémentation de version mineure (2.2.1 → 2.3.0)
   bump2version minor

   # Incrémentation de version majeure (2.2.1 → 3.0.0)
   bump2version major

**Ce qui se passe :**

1. Bump2version met à jour tous les numéros de version dans les fichiers configurés
2. Il crée automatiquement un commit avec l'incrémentation de version
3. Il crée un tag git pour la nouvelle version
4. Il met à jour le CHANGELOG.md avec une nouvelle entrée de version

**Notes importantes :**

- Mettez toujours à jour le CHANGELOG.md avec les changements avant d'incrémenter la version
- L'entrée CHANGELOG pour la nouvelle version sera créée automatiquement, mais vous devez ajouter les changements réels en dessous
- Après l'incrémentation, poussez à la fois le commit et le tag : ``git push && git push --tags``

Code de conduite
----------------

Notre engagement
~~~~~~~~~~~~~~~~

Dans l'intérêt de favoriser un environnement ouvert et accueillant, nous, en tant que contributeurs et mainteneurs, nous engageons à faire de la participation à notre projet et à notre communauté une expérience sans harcèlement pour tous, indépendamment de l'âge, de la taille corporelle, du handicap, de l'origine ethnique, de l'identité et de l'expression de genre, du niveau d'expérience, de la nationalité, de l'apparence personnelle, de la race, de la religion ou de l'orientation et identité sexuelles.

Nos standards
~~~~~~~~~~~~~

Les exemples de comportements qui contribuent à créer un environnement positif incluent :

- Utiliser un langage accueillant et inclusif
- Être respectueux des différents points de vue et expériences
- Accepter gracieusement les critiques constructives
- Se concentrer sur ce qui est le mieux pour la communauté
- Faire preuve d'empathie envers les autres membres de la communauté

Les exemples de comportements inacceptables de la part des participants incluent :

- L'utilisation de langage ou d'images sexualisés et d'attention ou d'avances sexuelles indésirables
- Le trolling, les commentaires insultants/désobligeants et les attaques personnelles ou politiques
- Le harcèlement public ou privé
- La publication d'informations privées d'autrui, telles qu'une adresse physique ou électronique, sans autorisation explicite
- Tout autre comportement qui pourrait raisonnablement être considéré comme inapproprié dans un cadre professionnel

Nos responsabilités
~~~~~~~~~~~~~~~~~~~

Les mainteneurs du projet sont responsables de clarifier les standards de comportement acceptable et sont censés prendre des mesures correctives appropriées et équitables en réponse à tout cas de comportement inacceptable.

Les mainteneurs du projet ont le droit et la responsabilité de supprimer, modifier ou rejeter les commentaires, commits, code, modifications du wiki, tickets et autres contributions qui ne sont pas alignés sur ce code de conduite, ou de bannir temporairement ou définitivement tout contributeur pour d'autres comportements qu'ils jugent inappropriés, menaçants, offensants ou nuisibles.

Champ d'application
~~~~~~~~~~~~~~~~~~~

Ce code de conduite s'applique à la fois dans les espaces du projet et dans les espaces publics lorsqu'un individu représente le projet ou sa communauté. Les exemples de représentation d'un projet ou d'une communauté incluent l'utilisation d'une adresse e-mail officielle du projet, la publication via un compte de médias sociaux officiel, ou l'action en tant que représentant désigné lors d'un événement en ligne ou hors ligne. La représentation d'un projet peut être davantage définie et clarifiée par les mainteneurs du projet.

Attribution
~~~~~~~~~~~

Ce code de conduite est adapté du `Contributor Covenant <http://contributor-covenant.org>`__, version 1.4, disponible à l'adresse `http://contributor-covenant.org/version/1/4 <http://contributor-covenant.org/version/1/4/>`__