Permissions
===========

Les permissions ou autorisations dans Django sont utilisées pour s'assurer que l'entité qui effectue la requête a le droit de lire/écrire la ressource. Par défaut, les classes d'entité sont définies sur ``django.contrib.auth.User``. Nous fournissons également une classe de permission qui, par défaut, garantit que seules les entités actives (``users``) ont la permission de lire/écrire la ressource.

.. code:: python

   class IsActiveEntity(BasePermission):
       """
       Une permission de base qui vérifie uniquement si l'entité (par défaut, l'utilisateur Django) est
       active ou non.
       """

       message = "L'entité n'est pas active."

       def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:

           return request.user.is_active

       def has_object_permission(
           self, request: HttpRequest, view: typing.Any, obj
       ) -> bool:

           return request.user.is_active

Vous pouvez ensuite utiliser cette classe dans votre vue 👇

.. code:: python

   from drf_simple_apikey.permissions import IsActiveEntity

   class YourViewSet(viewsets.ViewSet):
       ...
       authentication_classes = (APIKeyAuthentication, )
       permission_classes = (IsActiveEntity, )

N'hésitez pas à lire le code de la classe de permission sur
https://github.com/koladev32/drf-simple-apikey/blob/main/drf_simple_apikey/permissions.py.