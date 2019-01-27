class ModerationError(Exception):
    pass


class BadMessage(ModerationError):
    def __init__(self):
        self.message = 'Your post contains inappropriate text'.format()
        super().__init__(self.message)


class BadImage(ModerationError):
    def __init__(self):
        self.message = 'Your post contains inappropriate images'.format()
        super().__init__(self.message)


class Banned(ModerationError):
    def __init__(self, reason, active_until):
        self.message = 'You were banned for {} until {}'.format(reason, active_until)
        super().__init__(self.message)
