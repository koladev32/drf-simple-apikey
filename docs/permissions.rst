Permissions
===========

Permissions or authorization in Django are used to make sure the entity
making the request has the right to read/write the resource. By default,
entity classes are set to ``django.contrib.auth.User``. We also provide a permission class,
which by default ensures that only active entities ``users`` have
permission to read/write the resource.

.. code:: python

   class IsActiveEntity(BasePermission):
       """
       A base permission that only checks if the entity (by default, the Django user) is
       active or not.
       """

       message = "Entity is not active."

       def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:

           return request.user.is_active

       def has_object_permission(
           self, request: HttpRequest, view: typing.Any, obj
       ) -> bool:

           return request.user.is_active

You can then call use this class in your view 👇

.. code:: python

   from drf_simple_apikey.permissions import IsActiveEntity

   class YourViewSet(viewsets.ViewSet):
       ...
       authentication_classes = (APIKeyAuthentication, )
       permission_classes = (IsActiveEntity, )

Feel free to read the code of the permission class at
`https://github.com/koladev32/drf-simple-apikey/blob/main/drf-simple-apikey/permissions.py <https://github.com/koladev32/drf-simple-apikey/blob/main/drf-simple-apikey/backends.py>`__.
