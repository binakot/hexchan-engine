# Standard library imports
import os
import hashlib

# Django imports
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import get_user
from django.db import transaction, DatabaseError
from django.db.models import F, Subquery
from django.views.decorators.csrf import csrf_exempt

# Third party imports
import PIL.Image
import bleach

# App imports
from hexchan import config
from imageboard.models import Board, Thread, Post, Image
from imageboard.forms import PostingForm
from imageboard.views.parts import push_to_session_list
from imageboard import exceptions as i_ex
from imageboard.wakabamark import extract_refs
from captcha.interface import check_captcha, set_captcha
from captcha import exceptions as c_ex


@csrf_exempt
def posting_view(request):
    response = None

    # Check messsage contents and DB objects
    try:
        # Check request type
        if not request.POST:
            raise i_ex.BadRequestType

        # Get form data
        form = PostingForm(request.POST)
        if not form.is_valid():
            raise i_ex.FormValidationError(form.errors)

        # Check captcha
        check_captcha_for_request(request, form)

        # Get form type
        form_type = form.cleaned_data['form_type']

        # Get and check board object
        board_id = form.cleaned_data['board_id']
        board = get_board(board_id)

        #  If creating post in a thread - get and check that thread
        if form_type == 'new_post':
            # Get and check  thread
            thread_id = form.cleaned_data['thread_id']
            thread = get_thread(thread_id)
        else:
            thread = None

        # Get list of uploaded image objects
        images = request.FILES.getlist('images')

        # Check message
        check_message_content(cleaned_data=form.cleaned_data, images=images)

    except (i_ex.ImageboardError, c_ex.CaptchaError) as e:
        # Render error page if something went wrong
        response = render(request, 'imageboard/posting_error_page.html', context={'exception': e}, status=403)

    else:
        # Create thread, op post, save images, bump board's thread counter
        with transaction.atomic():
            # Bump board's post HID counter
            board.last_post_hid = (F('last_post_hid') + 1) if board.last_post_hid is not None else 0
            board.save()
            board.refresh_from_db()

            if form_type == 'new_thread':
                thread = create_thread(request, board)
                post = create_post(request, board, thread, form.cleaned_data, is_op=True)
                create_images(post, images)
                create_refs(request, board, thread, post)
                thread.op = post
                thread.save()
                flush_old_threads(request, board)
                push_to_session_list(request, 'user_posts', post.id)
                push_to_session_list(request, 'user_threads', thread.id)
            else:
                post = create_post(request, board, thread, form.cleaned_data)
                create_images(post, images)
                create_refs(request, board, thread, post)

                # Close thread if post limit is reached
                if thread.posts.count() >= thread.max_posts_num:
                    thread.is_locked = True

                thread.save()
                push_to_session_list(request, 'user_posts', post.id)
                push_to_session_list(request, 'user_thread_replies', thread.id)

        # Redirect to the current thread
        # TODO: make a form checkbox for selecting destination - board or thread
        response = redirect('thread_page', board_hid=board.hid, thread_hid=thread.hid)

    finally:
        # Set new captcha on both failures and successes
        set_captcha(request)

    return response


def get_board(board_id: int) -> Board:
    """Get valid Board model object."""
    try:
        board = Board.objects.get(id=board_id, is_deleted=False)
    except Board.DoesNotExist:
        raise i_ex.BoardNotFound

    # Check board status
    if board.is_locked:
        raise i_ex.BoardIsLocked

    return board


def get_thread(thread_id: int) -> Thread:
    """Get valid Thread model object."""
    try:
        thread = Thread.objects.get(id=thread_id, is_deleted=False)
    except Thread.DoesNotExist:
        raise i_ex.ThreadNotFound

    # Check thread status
    if thread.is_locked:
        raise i_ex.ThreadIsLocked

    # Check thread posts num
    if thread.posts.count() >= thread.max_posts_num:
        raise i_ex.PostLimitWasReached

    return thread


def check_message_content(cleaned_data, images):
    # Check honeypot. Yes, the email field is a honeypot!
    if len(cleaned_data['email']) > 0:
        raise i_ex.BadMessageContent

    # Check if empty message
    if not cleaned_data['text'] and not images:
        raise i_ex.MessageIsEmpty

    # Check number of files
    if len(images) > config.FILE_MAX_NUM:
        raise i_ex.TooManyFiles

    # Check file(s) for field 'file'
    for file_object in images:
        if file_object.size > config.FILE_MAX_SIZE:
            raise i_ex.FileIsTooLarge
        if file_object.content_type not in config.FILE_MIME_TYPES:
            raise i_ex.BadFileType

    # TODO: remember to check password with regex when saving it


def get_client_ip(request) -> str:
    """Get real client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_images(post: Post, images) -> None:
    """Save all images in request."""
    for image_file in images:
        # Load image with PIL library
        image_pil_object = PIL.Image.open(image_file)

        # Create thumbnail with PIL library
        # Convert image to RGBA format when needed (for example, if image has indexed pallette 8bit per pixel mode)
        thumbnail_pil_object = image_pil_object.convert('RGBA')
        thumbnail_pil_object.thumbnail(config.IMAGE_THUMB_SIZE)

        # Calculate checksum
        checksum = hashlib.md5()
        for chunk in image_file.chunks(config.IMAGE_CHUNK_SIZE):
            checksum.update(chunk)

        # Create Django image object
        image = Image(
            post=post,

            original_name=image_file.name,
            mimetype=image_file.content_type,
            size=image_file.size,
            width=image_pil_object.width,
            height=image_pil_object.height,

            checksum=checksum.hexdigest(),

            thumb_width=thumbnail_pil_object.width,
            thumb_height=thumbnail_pil_object.height,
        )

        # Save image to the database
        image.save()

        # Save image to the disk
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.path())
        with open(image_full_path, 'wb+') as destination:
            for chunk in image_file.chunks(config.IMAGE_CHUNK_SIZE):
                destination.write(chunk)

        # Save thumbnail to the disk
        image_thumb_full_path = os.path.join(settings.MEDIA_ROOT, image.thumb_path())
        thumbnail_pil_object.save(image_thumb_full_path, "PNG")


def create_thread(request, board: Board) -> Thread:
    thread = Thread(
        hid=board.last_post_hid,
        board=board,
        max_posts_num=board.default_max_posts_num,
    )
    thread.save()
    return thread


def create_post(request, board: Board, thread: Thread, cleaned_data: dict, is_op: bool = False) -> Post:
    title = bleach.clean(cleaned_data['title'])
    author = bleach.clean(cleaned_data['author'])
    email = bleach.clean(cleaned_data['email'])
    text = bleach.clean(cleaned_data['text'])
    password = cleaned_data['password']

    post = Post(
        hid=board.last_post_hid,
        thread=thread,

        text=text,
        title=title,
        author=author,
        email=email,  # TODO: save emails
        password=password,  # TODO: save passwords

        is_op=is_op,

        created_by=get_user(request) if request.user.is_authenticated else None,

        ip_address=get_client_ip(request),
        session_id=request.session.session_key,
    )
    post.save()
    return post


def create_refs(request, board, thread, post):
    ref_ids = extract_refs(post.text)
    ref_posts = Post.objects.filter(thread__board=board, hid__in=ref_ids)
    post.refs.add(*ref_posts)


def check_captcha_for_request(request, form):
    captcha_data = form.cleaned_data['captcha']
    captcha_public_id = captcha_data.get('public_id')
    captcha_solution = captcha_data.get('solution')

    if request.user.is_authenticated:
        pass
    else:
        check_captcha(request, captcha_public_id, captcha_solution)


def flush_old_threads(request, board):
    if board.threads.count() > board.max_threads_num:
        old_threads = Thread.objects \
            .filter(board=board, is_deleted=False) \
            .order_by('board', '-is_sticky', '-hid')[board.max_threads_num:]

        for thread in old_threads:
            thread.is_locked = True
            thread.is_deleted = True
            thread.save()
