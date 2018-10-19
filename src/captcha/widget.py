from django import forms
from django.forms import Widget, MultiWidget, MultiValueField, HiddenInput


class CaptchaImageWidget(HiddenInput):
    template_name = 'captcha/captcha_image_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['image'] = value.image
        return context

    def format_value(self, value):
        return value.public_id


class CaptchaWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            # forms.HiddenInput(),
            CaptchaImageWidget(),
            forms.TextInput(attrs={'maxlength': 128}),
        )

        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value['challenge'], value['solution']]
        else:
            return [None, None]


class CaptchaField(MultiValueField):
    widget = CaptchaWidget

    def __init__(self, **kwargs):
        fields = (
            forms.CharField(),  # Captcha object
            forms.CharField(),  # Captcha solution
        )

        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        return {
            'challenge': data_list[0],
            'solution': data_list[1],
        }
