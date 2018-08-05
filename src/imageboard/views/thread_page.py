from django.http import HttpResponse


def thread_page(request, board_hid, thread_hid):
    return HttpResponse('thread_page {} {}'.format(board_hid, thread_hid))
