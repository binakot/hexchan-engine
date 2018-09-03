# Standard library imports
# import logging
import os
from typing import Union, Tuple

# Django imports
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user
from django.db import transaction, IntegrityError
from django.db.models import F

# Third party imports
import PIL.Image
import bleach

# App imports
from gensokyo import config
from imageboard.models import Board, Thread, Post, Image
from imageboard.forms import PostingForm


def posting_view(request):
    # Check request type
    if not request.POST:
        return handle_error('wrong_request_type')

    # Get form data
    form = PostingForm(request.POST)
    if not form.is_valid():
        return handle_error('form_is_invalid', form.errors.as_data)

    # Get form type
    form_type = form.cleaned_data['form_type']

    # Get and check board object
    board_id = form.cleaned_data['board_id']
    board, board_error = get_board(board_id)
    if board_error:
        return handle_error(board_error)

    #  If creating post in a thread - get and check that thread
    if form_type == 'new_post':
        thread_id = form.cleaned_data['thread_id']
        thread, thread_error = get_thread(thread_id)
        if thread_error:
            return handle_error(thread_error)
    else:
        thread = None

    # # Check captcha
    # captcha_error = check_captcha(request)
    # if captcha_error:
    #     return make_error_message(captcha_error)

    # Get list of uploaded image objects
    images = request.FILES.getlist('images')

    # Check message
    message_error = check_message_content(cleaned_data=form.cleaned_data, images=images)
    if message_error:
        return handle_error(message_error)

    # Create thread, op post, save images, bump board's thread counter
    try:
        with transaction.atomic():
            # Bump board's post HID counter
            board.last_post_hid = F('last_post_hid') + 1
            board.save()
            board.refresh_from_db()

            if form_type == 'new_thread':
                thread = create_thread(request, board)
                post = create_post(request, board, thread, form.cleaned_data, is_op=True)
                save_images(post, images)
                thread.op = post
                thread.save()

            elif form_type == 'new_post':
                post = create_post(request, board, thread, form.cleaned_data)

            else:
                return handle_error('unknow_form_type')

    # Handle database errors
    except IntegrityError as integrity_error:
        print(integrity_error)  # TODO LOGGING
        return handle_error('database_is_broken')

    # Handle file saving errors
    except IOError as io_error:
        print(io_error)  # TODO LOGGING
        return handle_error('storage_is_broken')

    # Handle missing boards
    except Board.DoesNotExist:
        return handle_error('board_not_found')

    # Handle missing threads
    except Thread.DoesNotExist:
        return handle_error('thread_not_found')

    # Redirect to the new thread or post
    if form_type == 'new_post':
        return redirect('thread_page', board_hid=board.hid, thread=thread.hid)
    elif form_type == 'new_thread':
        return redirect('board_page', board_hid=board.hid)
    else:
        return handle_error('missing_parameter')


def handle_error(message: str, data=None):
    print('ERROR', message, data)
    return redirect('error_page')


def get_board(board_id: int) -> Tuple[Union[Board, None], Union[str, None]]:
    """Get valid Board model object."""

    if board_id is None:
        return None, 'missing_parameter'

    board = Board.objects.get(id=board_id, is_deleted=False)

    # Check board status
    if board.is_locked:
        return None, 'board_is_closed'

    return board, None


def get_thread(thread_id: int) -> Tuple[Union[Thread, None], Union[str, None]]:
    """Get valid Thread model object."""

    if thread_id is None:
        return None, 'missing_parameter'

    thread = Thread.objects.get(id=thread_id, is_deleted=False)

    # Check thread status
    if thread.is_locked:
        return None, 'thread_is_closed'

    # Check thread posts num
    if thread.posts.count() >= thread.max_posts_num:
        return None, 'post_limit_is_reached'

    return thread, None


def check_message_content(cleaned_data, images) -> Union[str, None]:
    # Check honeypot. Yes, the email field is a honeypot!
    if len(cleaned_data['email']) > 0:
        return 'content_is_invalid'

    # Check if empty message
    if not cleaned_data['text'] and not images:
        return 'empty_message'

    # Check number of files
    if len(images) > config.FILE_MAX_NUM:
        return 'too_many_files'

    # Check file(s) for field 'file'
    for file_object in images:
        if file_object.size > config.FILE_MAX_SIZE:
            return 'file_is_too_large'
        if file_object.content_type not in config.FILE_MIME_TYPES:
            return 'invalid_file_type'

    # TODO: remember to check password with regex when saving it

    # If everything is OK return None
    return None


def get_client_ip(request) -> str:
    """Get real client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_images(post: Post, images) -> None:
    """Save all images in request."""
    for image_file in images:
        # Load image with PIL library
        image_pil_object = PIL.Image.open(image_file)

        # Create thumbnail with PIL library
        thumbnail_pil_object = image_pil_object.copy()
        thumbnail_pil_object.thumbnail(config.IMAGE_THUMB_SIZE)

        # Create Django image object
        image = Image(
            post=post,

            original_name=image_file.name,
            mimetype=image_file.content_type,
            size=image_file.size,
            width=image_pil_object.width,
            height=image_pil_object.height,

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
    )
    post.save()
    return post
