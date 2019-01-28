from django.apps import AppConfig
from django.db.models.signals import post_delete
from django.utils.translation import gettext_lazy as _

from imageboard.signals import image_delete_handler


class ImageboardConfig(AppConfig):
    name = 'imageboard'
    verbose_name = _('Imageboard')

    def ready(self):
        # Connect signals when app is ready
        post_delete.connect(image_delete_handler, sender='imageboard.Image')
