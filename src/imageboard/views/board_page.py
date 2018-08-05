from django.http import HttpResponse


def board_page(request, board_hid):
    return HttpResponse('board_page {}'.format(board_hid))
