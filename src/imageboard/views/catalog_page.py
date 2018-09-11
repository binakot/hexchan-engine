# Django imports
from django.shortcuts import render
from django.db.models import Prefetch, Count
from django.http import Http404

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

    # Return rendered template
    return render(request, 'imageboard/catalog_page.html', {
        'board': board,
        'boards': boards,
        'threads': threads,
    })

