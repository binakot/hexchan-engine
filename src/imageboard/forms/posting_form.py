from django import forms


class PostingForm(forms.Form):
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

    # email = forms.CharField(
    #     max_length=32, required=False, label='Почта'
    # )

    text = forms.CharField(
        max_length=2048, required=False, label='Текст',
        widget=forms.Textarea
    )

    # password = forms.CharField(
    #     max_length=16, required=False, label='Пароль'
    # )

    # captcha_id = forms.CharField(
    #     widget=forms.HiddenInput
    # )

    # captcha_response = forms.CharField(
    #     max_length=8, required=True, label='Капча'
    # )

    images = forms.FileField(
        required=False, label='Картинки',
        widget=forms.FileInput(attrs={'multiple': True})
    )
