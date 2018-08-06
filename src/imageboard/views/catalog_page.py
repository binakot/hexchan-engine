from django.shortcuts import render


def catalog_page(request, board_hid):
    return render(request, 'imageboard/catalog_page.html', {'board': board_hid})
