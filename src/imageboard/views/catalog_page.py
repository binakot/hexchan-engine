from django.http import HttpResponse


def catalog_page(request, board_hid):
    return HttpResponse('catalog_page {}'.format(board_hid))
