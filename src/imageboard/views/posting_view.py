# Django imports
from django.shortcuts import render, redirect
from django.db.models import Prefetch


# App imports
from imageboard.models import Board, Thread, Post
from imageboard.forms import PostingForm


def posting_view(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            print('FORM', form.cleaned_data)

            form_type = form.cleaned_data['form_type']
            board_id = form.cleaned_data['board_id']
            thread_id = form.cleaned_data['thread_id']
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            text = form.cleaned_data['text']

            board = Board.objects.get(id=board_id)
            if form_type == 'new_post':
                thread = Thread.objects.get(id=thread_id)
                print(board, thread)
                return redirect('thread_page', board_hid=board.hid, thread=thread.hid)
            else:
                thread = None
                print(board, thread)
                return redirect('board_page', board_hid=board.hid)
        else:
            print('ERRORS', form.errors)
            return redirect('error_page')
    else:
        return redirect('error_page')

