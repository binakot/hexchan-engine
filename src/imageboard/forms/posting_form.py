from django import forms
from django.utils.translation import gettext_lazy as _, pgettext_lazy

from hexchan import config
from imageboard.forms.textarea_widget import TextareaWidget
from captcha.widget import CaptchaField

###
# https://django.readthedocs.io/en/stable/topics/http/file-uploads.html#uploading-multiple-files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
###

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
        max_length=64, required=False, label=_('Title')
    )

    author = forms.CharField(
        max_length=32, required=False, label=_('Author')
    )

    email = forms.CharField(
        max_length=32, required=False, label=_('E-mail'),
        widget=forms.HiddenInput  # TODO: make visible, use email widget
    )

    text = forms.CharField(
        max_length=2048, required=False, label=_('Text'),
        widget=TextareaWidget
    )

    password = forms.CharField(
        max_length=16, required=False, label=_('Password'),
        widget=forms.HiddenInput  # TODO: make visible
    )

    captcha = CaptchaField(
        label=_('Captcha'), required=True
    )

    images = MultipleFileField(
        required=False, label=pgettext_lazy('posting form', 'Images'),
        widget=MultipleFileInput(attrs={
            'accept': ','.join(config.FILE_MIME_TYPES)
        })
    )

    def clean(self):
        # Get clean data
        cleaned_data = super().clean()

        # Check form type
        form_type = cleaned_data.get('form_type')
        if form_type not in ['new_thread', 'new_post']:
            raise forms.ValidationError(_('Incorrect form type'), code='invalid')

        # Check thread id when creating a new post
        thread_id = cleaned_data.get("thread_id")
        if form_type == 'new_post' and not thread_id:
            raise forms.ValidationError(_('Thread ID is not specified when creating a new post'), code='invalid')
