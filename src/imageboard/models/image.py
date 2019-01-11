from django.db import models
from django.conf import settings

from gensokyo import config


class Image(models.Model):
    """docstring for Image"""
    post = models.ForeignKey('Post', related_name='images', on_delete=models.CASCADE, db_index=True)

    original_name = models.CharField(max_length=128, editable=False)
    mimetype = models.CharField(max_length=16, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    size = models.IntegerField(editable=False)
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    is_spoiler = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, db_index=True)

    checksum = models.CharField(max_length=32, editable=False, blank=True)

    thumb_width = models.IntegerField(editable=False)
    thumb_height = models.IntegerField(editable=False)

    class Meta:
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
