# Standard import
import datetime

# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Count
from django.http import HttpResponse, Http404
from django.core.cache import cache

# App imports
from imageboard.models import Board, Thread


def catalog_page(request, board_hid):
    # Get boards
    boards = Board.objects.order_by('hid').all()

    # Get current board
    try:
        board = boards.get(hid=board_hid, is_deleted=False)
    except Board.DoesNotExist:
        raise Http404('Board not found')

    # Get cached page if exists and return it
    cache_key = 'catalog_page__{board_hid}'.format(board_hid=board_hid)
    cache_record = cache.get(cache_key)
    if cache_record is not None and not request.user.is_authenticated:
        timestamp, rendered_template = cache_record
        if board.updated_at == timestamp:
            return HttpResponse(rendered_template)

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('op'),
        Prefetch('op__images'),
    ]

    # Threads queryset
    threads = Thread.objects \
        .filter(board=board, is_deleted=False)\
        .select_related('board') \
        .prefetch_related(*prefetch_args) \
        .annotate(posts_count=Count('posts'))\
        .order_by('board', '-is_sticky', '-hid')

    # Cache data
    cache_data = {
        'updated_at': board.updated_at,
        'generated_at': datetime.datetime.now(),
        'board': board,
    }

    # Render template
    rendered_template = render_to_string(
        'imageboard/catalog_page.html',
        {
            'board': board,
            'boards': boards,
            'threads': threads,
            'cache_data': cache_data,
        },
        request,
    )

    # Write page to cache
    if not request.user.is_authenticated:
        new_cache_record = (board.updated_at, rendered_template,)
        cache.set(cache_key, new_cache_record)

    # Return response
    return HttpResponse(rendered_template)
