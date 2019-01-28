from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientErrorsConfig(AppConfig):
    name = 'client_errors'
    verbose_name = _('Client errors')
