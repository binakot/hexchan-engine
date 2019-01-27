from django.db import models
from django.conf import settings


class Ban(models.Model):
    BAN_TYPE_IP = 'ip'
    BAN_TYPE_NET = 'network'
    BAN_TYPE_SESSION = 'session'

    BAN_TYPES = (
        (BAN_TYPE_IP, 'IP address'),
        (BAN_TYPE_NET, 'Network'),
        (BAN_TYPE_SESSION, 'Session'),
    )

    type = models.CharField(
        max_length=8,
        choices=BAN_TYPES,
    )
    value = models.CharField(max_length=32)
    reason = models.ForeignKey('BanReason', on_delete=models.SET_NULL, null=True)
    active_until = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)


class BanReason(models.Model):
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.description


class WordFilter(models.Model):
    expression = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)


class ImageFilter(models.Model):
    checksum = models.CharField(max_length=32)
    size = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
