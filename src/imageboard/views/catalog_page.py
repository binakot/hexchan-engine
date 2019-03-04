# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Count
from django.http import HttpResponse

# App imports
from imageboard.models import Thread
from imageboard.views import parts
from imageboard.views.parts import CacheInterface, prefetch_posts_related_data


def catalog_page(request, board_hid):
    # Create response object
    response = HttpResponse()

    # Send some user session data as cookies
    parts.set_session_data_as_cookie(request, response, 'user_threads')
    parts.set_session_data_as_cookie(request, response, 'user_posts')
    parts.set_session_data_as_cookie(request, response, 'user_thread_replies')

    # Get boards
    boards = parts.get_boards()

    # Get current board
    board = parts.get_board(board_hid)

    # Create cache interface
    cache_interface = CacheInterface(
        key='catalog_page__{board_hid}'.format(board_hid=board_hid),
        obj=board,
        is_admin=request.user.is_authenticated
    )

    # Get cached page if exists and return it
    cached_template = cache_interface.get_cached_template()
    if cached_template:
        response.write(cached_template)
        return response

    prefetch_args = prefetch_posts_related_data('op')

    # Threads queryset
    threads = Thread.objects \
        .filter(board=board, is_deleted=False)\
        .select_related('board') \
        .prefetch_related(*prefetch_args) \
        .annotate(posts_count=Count('posts'))\
        .order_by('-is_sticky', '-updated_at')[:board.max_threads_num]

    # Cache data
    cache_data = cache_interface.make_cache_info(board=board)

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
    cache_interface.write_template_to_cache(rendered_template)

    # Return response
    response.write(rendered_template)
    return response
