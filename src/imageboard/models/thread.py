from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from hexchan import config


class Thread(models.Model):
    hid = models.IntegerField(
        _('HID'),
        editable=False,
        db_index=True
    )

    board = models.ForeignKey(
        'Board',
        verbose_name=_('Board'),
        related_name='threads',
        on_delete=models.CASCADE,
        db_index=True
    )

    # NOTE: 'plus' sign for 'related_name' disables reverse lookup, we don't need it here.
    # see: https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ForeignKey.related_name
    op = models.ForeignKey(
        'Post',
        verbose_name=_('OP'),
        on_delete=models.CASCADE,
        db_index=True,
        related_name='+',
        null=True
    )

    is_sticky = models.BooleanField(
        _('Is sticky'),
        default=False,
        db_index=True
    )

    is_locked = models.BooleanField(
        _('Is locked'),
        default=False,
        db_index=True
    )

    is_deleted = models.BooleanField(
        _('Is deleted'),
        default=False,
        db_index=True
    )

    max_posts_num = models.IntegerField(
        _('Maximum posts number')
    )

    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        editable=False,
        db_index=True
    )

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        editable=False,
        db_index=True
    )

    class Meta:
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')
        unique_together = ['board', 'hid']
        indexes = []
        ordering = ['-updated_at']

    def hid2hex(self):
        return config.THREAD_FULL_HID_FORMAT.format(hid=self.hid)

    def get_absolute_url(self):
        thread_url = reverse(
            'thread_page',
            kwargs={'board_hid': self.board.hid, 'thread_hid': self.hid}
        )

        return thread_url

