from django.shortcuts import render


def thread_page(request, board_hid, thread_hid):
    return render(request, 'imageboard/thread_page.html', {'board': board_hid, 'thread': thread_hid})
