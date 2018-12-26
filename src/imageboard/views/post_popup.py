# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# App imports
from imageboard.models import Board, Post
from gensokyo import config


@cache_page(config.CACHE_POST_POPUP)
def post_popup(request, board_hid, thread_hid, post_hid):
    # Get current board
    try:
        board = Board.objects.get(hid=board_hid, is_deleted=False)
    except Post.DoesNotExist:
        board = None

    # Refs and replies queryset
    refs_and_replies_queryset = Post.objects\
        .select_related('thread', 'thread__board')\
        .only('is_op', 'hid', 'thread__hid', 'thread__board__hid')

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('images'),
        Prefetch('refs', queryset=refs_and_replies_queryset),
        Prefetch('post_set', queryset=refs_and_replies_queryset, to_attr='replies'),
    ]

    # Get current post
    try:
        post = Post.objects\
            .prefetch_related(*prefetch_args)\
            .get(hid=post_hid, thread__hid=thread_hid, thread__board__hid=board_hid)
    except Post.DoesNotExist:
        post = None

    # Render template
    rendered_template = render_to_string(
        'imageboard/post_popup.html',
        {
            'board': board,
            'post': post,
            'is_popup': True,
        },
        request,
    )

    # Return response
    return HttpResponse(rendered_template)
