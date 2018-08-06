from django.shortcuts import render


def board_page(request, board_hid):
    return render(request, 'imageboard/board_page.html', {'board': board_hid})
