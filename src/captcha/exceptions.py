from django.utils.translation import gettext_lazy as _


class CaptchaError(Exception):
    pass


class CaptchaDbIsEmpty(CaptchaError):
    def __init__(self):
        self.message = _('Captcha DB is empty')
        super().__init__(self.message)


class CaptchaIsInvalid(CaptchaError):
    def __init__(self):
        self.message = _('Captcha is invalid')
        super().__init__(self.message)


class CaptchaHasExpired(CaptchaError):
    def __init__(self):
        self.message = _('Captcha has expired')
        super().__init__(self.message)


class CaptchaNotFound(CaptchaError):
    def __init__(self):
        self.message = _('Captcha not found')
        super().__init__(self.message)
