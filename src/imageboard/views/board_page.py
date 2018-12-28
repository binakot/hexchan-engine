# Standard import
import datetime

# Django imports
from django.template.loader import render_to_string
from django.db.models import Prefetch, Count, Subquery, OuterRef, Q
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.core.cache import cache

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm
from gensokyo import config


def board_page(request, board_hid, page_num=1):
    # Get boards
    boards = Board.objects.order_by('hid').all()

    # Get current board
    try:
        board = boards.get(hid=board_hid, is_deleted=False)
    except Board.DoesNotExist:
        raise Http404('Board not found')

    # Get cached page if exists and return it
    if config.CACHE_ENABLED:
        cache_key = 'board_page__{board_hid}__{page_num}'.format(board_hid=board_hid, page_num=page_num)
        cache_record = cache.get(cache_key)
        if cache_record is not None and not request.user.is_authenticated:
            timestamp, rendered_template = cache_record
            if board.updated_at == timestamp:
                return HttpResponse(rendered_template)

    # Queryset for latest posts
    latest_posts_queryset = Post.objects\
        .filter(thread=OuterRef('thread'), is_op=False)\
        .order_by('-id')\
        .values_list('id', flat=True)[:board.posts_per_thread_per_page]

    # Refs and replies queryset
    refs_and_replies_queryset = Post.objects\
        .select_related('thread', 'thread__board')\
        .only('is_op', 'hid', 'thread__hid', 'thread__board__hid')

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('posts', queryset=Post.objects.filter(
            Q(id__in=Subquery(latest_posts_queryset)) | Q(is_op=True))
        ),
        Prefetch('posts__images'),
        Prefetch('posts__refs', queryset=refs_and_replies_queryset),
        Prefetch('posts__post_set', queryset=refs_and_replies_queryset, to_attr='replies'),
    ]

    # Threads queryset
    threads = Thread.objects\
        .filter(board__hid=board_hid, is_deleted=False)\
        .select_related('board')\
        .prefetch_related(*prefetch_args)\
        .annotate(posts_count=Count('posts'))\
        .order_by('board', '-is_sticky', '-hid')[:board.max_threads_num]

    # Paginate threads
    paginator = Paginator(threads, board.threads_per_page)
    paginated_threads = paginator.get_page(page_num)

    # Add extra data
    for thread in paginated_threads:
        # Count skipped posts
        skipped = thread.posts_count - (board.posts_per_thread_per_page + 1)
        thread.skipped = max(skipped, 0)

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
    cache_data = {
        'updated_at': board.updated_at,
        'generated_at': datetime.datetime.now(),
        'board': board.hid,
        'page': page_num,
    } if config.CACHE_ENABLED else None

    # Render template
    rendered_template = render_to_string(
        'imageboard/board_page.html',
        {
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
    if config.CACHE_ENABLED and not request.user.is_authenticated:
        new_cache_record = (board.updated_at, rendered_template,)
        cache.set(cache_key, new_cache_record)

    # Return response
    return HttpResponse(rendered_template)
