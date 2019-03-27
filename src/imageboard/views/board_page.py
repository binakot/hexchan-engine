# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Count, Subquery, OuterRef, Q
from django.core.paginator import Paginator
from django.http import HttpResponse

# App imports
from imageboard.models import Thread, Post
from imageboard.views import parts
from imageboard.views.parts import CacheInterface, prefetch_posts_related_data
from imageboard.forms import PostingForm


def board_page(request, board_hid, page_num=1):
    # Create response object
    response = HttpResponse()

    # Send some user session data as cookies
    parts.set_session_data_as_cookie(request, response, 'user_threads')
    parts.set_session_data_as_cookie(request, response, 'user_posts')
    parts.set_session_data_as_cookie(request, response, 'user_thread_replies')

    # Get boards
    boards = parts.get_boards()

    # Get current board
    board = parts.get_board(board_hid)

    # Create cache interface
    cache_interface = CacheInterface(
        key='board_page__{board_hid}__{page_num}'.format(board_hid=board_hid, page_num=page_num),
        obj=board,
        is_admin=request.user.is_authenticated
    )

    # Get cached page if exists and return it
    cached_template = cache_interface.get_cached_template()
    if cached_template:
        response.write(cached_template)
        return response

    # Queryset for latest posts
    latest_posts_queryset = Post.objects\
        .filter(thread=OuterRef('thread'), is_deleted=False, is_op=False)\
        .order_by('-id')\
        .values_list('id', flat=True)[:board.posts_per_thread_per_page]

    visible_posts_queryset = Post.objects.filter(Q(id__in=Subquery(latest_posts_queryset)) | Q(is_op=True))

    prefetch_args = prefetch_posts_related_data('posts', posts_queryset=visible_posts_queryset)

    # Threads queryset
    threads = Thread.objects\
        .filter(board__hid=board_hid, is_deleted=False)\
        .select_related('board')\
        .prefetch_related(*prefetch_args)\
        .annotate(posts_count=Count('posts'))\
        .order_by('-is_sticky', '-updated_at')[:board.max_threads_num]

    # Paginate threads
    paginator = Paginator(threads, board.threads_per_page)
    paginated_threads = paginator.get_page(page_num)

    # Add extra data
    for thread in paginated_threads:
        thread.latest_posts = []
        for post in thread.posts.all():
            if post.is_op:
                thread.op = post
            else:
                thread.latest_posts.append(post)

    # Init thread creation form
    form = PostingForm(
        initial={
            'form_type': 'new_thread',
            'board_id': board.id,
        },
    )

    # Cache data
    cache_data = cache_interface.make_cache_info(board=board, page=page_num)

    # Render template
    rendered_template = render_to_string(
        'imageboard/board_page.html',
        {
            'page_type': 'board_page',
            'form': form,
            'board': board,
            'boards': boards,
            'threads': paginated_threads,
            'page': page_num,
            'cache_data': cache_data,
        },
        request
    )

    # Write page to cache
    cache_interface.write_template_to_cache(rendered_template)

    # Return response
    response.write(rendered_template)
    return response
