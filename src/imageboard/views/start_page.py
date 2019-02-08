# Django imports
from django.http import HttpResponse
from django.template.loader import render_to_string

# App imports
from imageboard.models import Board
from imageboard.views.parts import set_session_data_as_cookie


def start_page(request):
    # Create response object
    response = HttpResponse()

    # Send some user session data as cookies
    set_session_data_as_cookie(request, response, 'user_threads')
    set_session_data_as_cookie(request, response, 'user_posts')
    set_session_data_as_cookie(request, response, 'user_thread_replies')

    # Get boards
    boards = Board.objects.order_by('hid').filter(is_deleted=False, is_hidden=False)

    rendered_template = render_to_string(
        'imageboard/start_page.html',
        {
            'boards': boards,
        },
        request
    )

    response.write(rendered_template)
    return response
