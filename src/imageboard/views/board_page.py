# Django imports
from django.shortcuts import render
from django.db.models import Prefetch, Count
from django.core.paginator import Paginator

# App imports
from imageboard.models import Board, Thread, Post, Image
from gensokyo import config


def board_page(request, board_hid, page_num=1):
    boards = Board.objects.order_by('hid').all()
    board = boards.get(hid=board_hid, is_deleted=False)

    # Combine prefetch args, also prefetch required images
    prefetch_args = [
        Prefetch('op'),
        Prefetch('op__images'),
        Prefetch('op__replies', queryset=Post.objects.only('id', 'hid')),
    ]

    # Threads queryset
    threads = Thread.objects\
        .filter(board__hid=board_hid, is_deleted=False)\
        .select_related('board')\
        .prefetch_related(*prefetch_args)\
        .annotate(posts_count=Count('posts'))\
        .order_by('board', '-is_sticky', '-hid')

    # Paginate threads
    paginator = Paginator(threads, config.THREADS_PER_PAGE)
    paginated_threads = paginator.get_page(page_num)

    # Add extra data
    for thread in paginated_threads:
        # Count skipped posts
        skipped = thread.posts_count - (config.POSTS_PER_THREAD_PER_PAGE + 1)
        thread.skipped = max(skipped, 0)

        # Get latest posts list
        latest_posts = Post.objects\
            .filter(thread=thread.id, is_op=False)\
            .prefetch_related(
                Prefetch('images'),
                Prefetch('replies', queryset=Post.objects.only('id', 'hid')),
            )\
            .order_by('-id')[:config.POSTS_PER_THREAD_PER_PAGE]

        latest_posts_list = list(latest_posts)
        latest_posts_list.reverse()

        thread.latest_posts = latest_posts_list

    # Return rendered template
    return render(request, 'imageboard/board_page.html', {
        'board': board,
        'boards': boards,
        'threads': paginated_threads,
        'page': page_num,
    })
