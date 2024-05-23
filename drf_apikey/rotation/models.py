from django.db import models


class Rotation(models.Model):
    is_rotation_enabled = models.BooleanField(default=False)
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)
