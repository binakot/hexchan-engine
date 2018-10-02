from django.shortcuts import render

from imageboard.models import Board, Thread, Post


def start_page(request):
    # Get boards
    boards = Board.objects.order_by('hid').filter(is_deleted=False, is_hidden=False)

    return render(
        request,
        'imageboard/start_page.html',
        {
            'boards': boards,
        }
    )
