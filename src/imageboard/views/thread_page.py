# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import HttpResponse

# App imports
from imageboard.models import Thread, Post
from imageboard.forms import PostingForm
from imageboard.views import parts
from imageboard.views.parts import CacheInterface


def thread_page(request, board_hid, thread_hid):
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

    # Thread queryset
    thread = parts.get_thread(board_hid, thread_hid)

    # Create cache interface
    cache_interface = CacheInterface(
        key='thread_page__{board_hid}__{thread_hid}'.format(board_hid=board_hid, thread_hid=thread_hid),
        obj=thread,
        is_admin=request.user.is_authenticated
    )

    # Get cached page if exists and return it
    cached_template = cache_interface.get_cached_template()
    if cached_template:
        response.write(cached_template)
        return response

    # Refs and replies queryset
    refs_and_replies_queryset = Post.objects\
        .select_related('thread', 'thread__board')\
        .only('is_op', 'hid', 'thread__hid', 'thread__board__hid')

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('posts'),
        Prefetch('posts__images'),
        Prefetch('posts__refs', queryset=refs_and_replies_queryset),
        Prefetch('posts__post_set', queryset=refs_and_replies_queryset, to_attr='replies'),
        Prefetch('posts__created_by'),
    ]

    # Prefetch stuff for the thread
    thread = Thread.objects\
        .select_related('board')\
        .prefetch_related(*prefetch_args) \
        .get(board__hid=board_hid, hid=thread_hid, is_deleted=False)

    # Add extra data
    all_posts = thread.posts.all()
    thread.op = all_posts[0]
    thread.other_posts = all_posts[1:]

    # Init post creation form
    form = PostingForm(
        initial={
            'form_type': 'new_post',
            'board_id': board.id,
            'thread_id': thread.id,
        },
    )

    # Cache data
    cache_data = cache_interface.make_cache_info(board=board, thread=thread)

    # Render template
    rendered_template = render_to_string(
        'imageboard/thread_page.html',
        {
            'form': form,
            'board': board,
            'boards': boards,
            'thread': thread,
            'cache_data': cache_data,
        },
        request
    )

    # Write page to cache
    cache_interface.write_template_to_cache(rendered_template)

    # Return response
    response.write(rendered_template)
    return response
