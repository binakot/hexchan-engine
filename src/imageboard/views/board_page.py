# Django imports
from django.shortcuts import render
from django.db.models import Prefetch, Count, Subquery, OuterRef
from django.core.paginator import Paginator
from django.http import Http404

# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm
from imageboard.errors import codes
from gensokyo import config


def board_page(request, board_hid, page_num=1):
    # Get boards
    boards = Board.objects.order_by('hid').all()

    # Get current board
    try:
        board = boards.get(hid=board_hid, is_deleted=False)
    except Board.DoesNotExist:
        raise Http404(codes.BOARD_NOT_FOUND)

    # Queryset for latest posts
    latest_posts_queryset = Post.objects\
        .filter(thread=OuterRef('thread'), is_op=False)\
        .order_by('-id')\
        .values_list('id', flat=True)[:config.POSTS_PER_THREAD_PER_PAGE]

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('op'),
        Prefetch('op__images'),
        Prefetch('op__replies', queryset=Post.objects.only('id', 'hid')),
        Prefetch('posts', queryset=Post.objects.filter(id__in=Subquery(latest_posts_queryset)), to_attr='latest_posts'),
        Prefetch('latest_posts__images'),
        Prefetch('latest_posts__replies', queryset=Post.objects.only('id', 'hid')),
    ]

    # Threads queryset
    threads = Thread.objects\
        .filter(board__hid=board_hid, is_deleted=False)\
        .select_related('board')\
        .prefetch_related(*prefetch_args)\
        .annotate(posts_count=Count('posts'))\
        .order_by('board', '-is_sticky', '-hid')[:config.MAX_PAGES * config.THREADS_PER_PAGE]

    # Paginate threads
    paginator = Paginator(threads, config.THREADS_PER_PAGE)
    paginated_threads = paginator.get_page(page_num)

    # Add extra data
    for thread in paginated_threads:
        # Count skipped posts
        skipped = thread.posts_count - (config.POSTS_PER_THREAD_PER_PAGE + 1)
        thread.skipped = max(skipped, 0)

        latest_posts_list = list(thread.latest_posts)
        latest_posts_list.reverse()

        thread.latest_posts = latest_posts_list

    # Init thread creation form
    form = PostingForm(
        initial={
            'form_type': 'new_thread',
            'board_id': board.id
        },
    )

    # Return rendered template
    return render(request, 'imageboard/board_page.html', {
        'form': form,
        'board': board,
        'boards': boards,
        'threads': paginated_threads,
        'page': page_num,
    })
