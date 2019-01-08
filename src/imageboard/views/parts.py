# Standard imports
import datetime
from typing import List

# Django imports
from django.http import Http404
from django.core.cache import cache

# App imports
from gensokyo import config
from imageboard.models import Board, Thread


def get_session_list(request, session_key: str, limit=16) -> List[int]:
    return request.session.get(session_key, [])[-limit:]


def push_to_session_list(request, session_key: str, value: int, limit=16) -> None:
    session_list = request.session.get(session_key, [])[-(limit-1):]
    session_list.append(value)
    request.session[session_key] = session_list


def set_session_data_as_cookie(request, response, session_key: str):
    session_list = get_session_list(request, session_key)
    data_string = '#'.join([str(x) for x in session_list])
    response.set_cookie(session_key, data_string)


def get_boards():
    """Get all boards."""
    return Board.objects.order_by('hid').filter(is_deleted=False, is_hidden=False)


def get_board(board_hid: str):
    """Get current board."""
    try:
        return Board.objects.get(hid=board_hid, is_deleted=False)
    except Board.DoesNotExist:
        raise Http404('Board not found')


def get_thread(board_hid: str, thread_hid: str):
    """Thread queryset."""
    try:
        return Thread.objects.get(board__hid=board_hid, hid=thread_hid, is_deleted=False)
    except Thread.DoesNotExist:
        raise Http404('Thread not found')


class CacheInterface:
    def __init__(self, key, obj):
        self.key = key
        self.obj = obj

    def get_cached_template(self):
        """Get cached page if exists and return it."""
        if config.CACHE_ENABLED:
            cache_record = cache.get(self.key)
            if cache_record is not None:
                timestamp, rendered_template = cache_record
                if self.obj.updated_at == timestamp:
                    return rendered_template

    def write_template_to_cache(self, rendered_template: str):
        """Write page to cache."""
        if config.CACHE_ENABLED:
            new_cache_record = (self.obj.updated_at, rendered_template,)
            cache.set(self.key, new_cache_record)

    def make_cache_info(self, **kwargs):
        """Make cache info for use in template."""
        if config.CACHE_ENABLED:
            cache_data = {
                'updated_at': self.obj.updated_at,
                'generated_at': datetime.datetime.now(),
            }
            cache_data.update(kwargs)
            return cache_data
