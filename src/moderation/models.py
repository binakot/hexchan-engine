from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Ban(models.Model):
    BAN_TYPE_IP = 'ip'
    BAN_TYPE_NET = 'network'
    BAN_TYPE_SESSION = 'session'

    BAN_TYPES = (
        (BAN_TYPE_IP, _('IP address')),
        (BAN_TYPE_NET, _('Network')),
        (BAN_TYPE_SESSION, _('Session')),
    )

    type = models.CharField(
        _('Type'),
        max_length=8,
        choices=BAN_TYPES,
    )

    value = models.CharField(
        _('Value'),
        max_length=32
    )

    reason = models.ForeignKey(
        'BanReason',
        verbose_name=_('Ban reason'),
        on_delete=models.SET_NULL,
        null=True
    )

    active_until = models.DateTimeField(
        _('Active until'),
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Created by'),
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = _('Ban')
        verbose_name_plural = _('Bans')


class BanReason(models.Model):
    description = models.CharField(
        _('Description'),
        max_length=256
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Ban reason')
        verbose_name_plural = _('Ban reasons')


class WordFilter(models.Model):
    expression = models.CharField(
        _('Regular expression'),
        max_length=256
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Created by'),
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = _('Word filter')
        verbose_name_plural = _('Word filters')


class ImageFilter(models.Model):
    checksum = models.CharField(
        _('Checksum'),
        max_length=32
    )

    size = models.IntegerField(
        _('Size'),
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Created by'),
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = _('Image filter')
        verbose_name_plural = _('Image filters')
