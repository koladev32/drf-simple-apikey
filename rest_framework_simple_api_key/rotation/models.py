from django.db import models


class RotationConfig(models.Model):
    is_rotation_enabled = models.BooleanField(default=False)
    last_rotation_date = models.DateTimeField(null=True, blank=True)
    next_rotation_date = models.DateTimeField(null=True, blank=True)

