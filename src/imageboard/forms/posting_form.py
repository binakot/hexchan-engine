from django import forms

from gensokyo import config


class PostingForm(forms.Form):
    # TODO: move constants to config?

    form_type = forms.CharField(
        widget=forms.HiddenInput
    )

    board_id = forms.IntegerField(
        widget=forms.HiddenInput
    )

    thread_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput
    )

    title = forms.CharField(
        max_length=64, required=False, label='Тема'
    )

    author = forms.CharField(
        max_length=32, required=False, label='Автор'
    )

    email = forms.CharField(
        max_length=32, required=False, label='Почта',
        widget=forms.HiddenInput  # TODO: make visible, use email widget
    )

    text = forms.CharField(
        max_length=2048, required=False, label='Текст',
        widget=forms.Textarea
    )

    password = forms.CharField(
        max_length=16, required=False, label='Пароль',
        widget=forms.HiddenInput  # TODO: make visible
    )

    # TODO: captcha
    # captcha_id = forms.CharField(
    #     widget=forms.HiddenInput
    # )

    # captcha_response = forms.CharField(
    #     max_length=8, required=True, label='Капча'
    # )

    images = forms.FileField(
        required=False, label='Картинки',
        widget=forms.FileInput(attrs={
            'multiple': True,
            'accept': ','.join(config.FILE_MIME_TYPES)
        })
    )

    def clean(self):
        # Get clean data
        cleaned_data = super().clean()

        # Check form type
        form_type = cleaned_data['form_type']
        if form_type not in ['new_thread', 'new_post']:
            raise forms.ValidationError('Incorrect form type', code='invalid')

        # Check thread id when creating a new post
        thread_id = cleaned_data.get("thread_id")
        if form_type == 'new_post' and not thread_id:
            raise forms.ValidationError('Thread ID is not specified when creating a new post', code='invalid')
