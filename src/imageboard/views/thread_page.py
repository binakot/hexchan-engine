# Django imports
from django.shortcuts import render
from django.db.models import Prefetch

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm


def thread_page(request, board_hid, thread_hid):
    boards = Board.objects.order_by('hid').all()
    board = boards.get(hid=board_hid, is_deleted=False)

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('op'),
        Prefetch('op__images'),
        Prefetch('op__replies', queryset=Post.objects.only('id', 'hid')),
        Prefetch('posts', queryset=Post.objects.filter(is_op=False)),
        Prefetch('posts__images'),
        Prefetch('posts__replies', queryset=Post.objects.only('id', 'hid')),
    ]

    # Thread queryset
    thread = Thread.objects \
        .select_related('board') \
        .prefetch_related(*prefetch_args) \
        .get(board__hid=board_hid, hid=thread_hid, is_deleted=False)

    # Init post creation form
    form = PostingForm(
        initial={
            'form_type': 'new_post',
            'board_id': board.id,
            'thread_id': thread.id
        },
    )

    # Return rendered template
    return render(request, 'imageboard/thread_page.html', {
        'form': form,
        'board': board,
        'boards': boards,
        'thread': thread,
    })
