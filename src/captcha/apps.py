from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CaptchaConfig(AppConfig):
    name = 'captcha'
    verbose_name = _('Captcha')
