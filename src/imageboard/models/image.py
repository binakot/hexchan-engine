from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from hexchan import config


class Image(models.Model):
    post = models.ForeignKey(
        'Post',
        verbose_name=_('Post'),
        related_name='images',
        on_delete=models.CASCADE,
        db_index=True
    )

    original_name = models.CharField(
        _('Original name'),
        max_length=128,
        editable=False
    )

    mimetype = models.CharField(
        _('MIME type'),
        max_length=16,
        editable=False
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False
    )

    size = models.IntegerField(
        _('Size'),
        editable=False
    )

    width = models.IntegerField(
        _('Width'),
        editable=False
    )

    height = models.IntegerField(
        _('Height'),
        editable=False
    )

    is_spoiler = models.BooleanField(
        _('Is spoiler'),
        default=False
    )

    is_deleted = models.BooleanField(
        _('Is deleted'),
        default=False,
        db_index=True
    )

    checksum = models.CharField(
        _('Checksum'),
        max_length=32,
        editable=False,
        blank=True
    )

    thumb_width = models.IntegerField(
        _('Thumb width'),
        editable=False
    )

    thumb_height = models.IntegerField(
        _('Thumb height'),
        editable=False
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        unique_together = []
        indexes = []

    def hid(self):
        return config.IMAGE_HID_FORMAT.format(hid=self.id) if self.id else '<empty>'

    def path(self):
        return '{dir}/{name}.{ext}'.format(
            dir=config.IMAGE_DIR,
            name=config.IMAGE_HID_FORMAT.format(hid=self.id),
            ext=config.IMAGE_EXTENSION[self.mimetype]
        ) if self.id else ''

    def thumb_path(self):
        return '{dir}/{name}.{ext}'.format(
            dir=config.THUMB_DIR,
            name=config.IMAGE_HID_FORMAT.format(hid=self.id),
            ext=config.THUMB_EXTENSION
        ) if self.id else ''
