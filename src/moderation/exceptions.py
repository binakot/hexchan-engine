from django.utils.translation import gettext_lazy as _


class ModerationError(Exception):
    pass


class BadMessage(ModerationError):
    def __init__(self):
        self.message = _('Your post contains inappropriate text')
        super().__init__(self.message)


class BadImage(ModerationError):
    def __init__(self):
        self.message = _('Your post contains inappropriate images')
        super().__init__(self.message)


class Banned(ModerationError):
    def __init__(self, reason, active_until):
        self.message = _(
            'You were banned for %(reason)s until %(active_until)s' %
            {'reason': reason, 'active_until': active_until}
        )
        super().__init__(self.message)
