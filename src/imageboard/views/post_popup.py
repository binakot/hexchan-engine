# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# App imports
from hexchan import config
from imageboard.models import Board, Post
from imageboard.views.parts import prefetch_posts_related_data


@cache_page(config.CACHE_POST_POPUP)
def post_popup(request, board_hid, thread_hid, post_hid):
    # Get current board
    try:
        board = Board.objects.get(hid=board_hid, is_deleted=False)
    except Post.DoesNotExist:
        board = None

    prefetch_args = prefetch_posts_related_data()

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
