class CaptchaError(Exception):
    pass


class CaptchaDbIsEmpty(CaptchaError):
    def __init__(self):
        self.message = 'Captcha DB is empty'.format()
        super().__init__(self.message)


class CaptchaIsInvalid(CaptchaError):
    def __init__(self):
        self.message = 'Captcha is invalid'.format()
        super().__init__(self.message)


class CaptchaHasExpired(CaptchaError):
    def __init__(self):
        self.message = 'Captcha has expired'.format()
        super().__init__(self.message)


class CaptchaNotFound(CaptchaError):
    def __init__(self):
        self.message = 'Captcha not found'.format()
        super().__init__(self.message)
