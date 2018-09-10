from django.apps import AppConfig
from django.db.models.signals import post_delete

from imageboard.signals import image_delete_handler


class ImageboardConfig(AppConfig):
    name = 'imageboard'

    def ready(self):
        # Connect signals when app is ready
        post_delete.connect(image_delete_handler, sender='imageboard.Image')
