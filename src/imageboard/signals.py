import os

from django.conf import settings
from django.core.files.storage import default_storage


def image_delete_handler(sender, **kwargs):
    image = kwargs.get('instance')

    # Remove image file
    image_full_path = os.path.join(settings.MEDIA_ROOT, image.path())
    default_storage.delete(image_full_path)

    # Remove thumbs
    image_full_thumb_path = os.path.join(settings.MEDIA_ROOT, image.thumb_path())
    default_storage.delete(image_full_thumb_path)
