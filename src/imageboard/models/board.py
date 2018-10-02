from django.db import models
from django.urls import reverse


class Board(models.Model):
    """docstring for Board"""
    hid = models.CharField(max_length=8, db_index=True)

    name = models.CharField(max_length=64)
    url = models.CharField(max_length=16)
    description = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    custom_style = models.TextField(blank=True)
    default_username = models.CharField(max_length=32)
    default_max_posts_num = models.IntegerField()

    is_hidden = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    last_post_hid = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.hid

    def threads_count(self):
        return self.threads.count()

    def get_absolute_url(self):
        return reverse('board_page', kwargs={'board_hid': self.hid})
