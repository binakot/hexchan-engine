from django.db import models


class Captcha(models.Model):
    """docstring for Captcha"""

    public_id = models.CharField(max_length=32)
    solution = models.CharField(max_length=32)
    image = models.TextField()
