class ImageboardError(Exception):
    pass


class BoardNotFound(ImageboardError):
    def __init__(self):
        self.message = 'Board not found'.format()
        super().__init__(self.message)


class BoardIsLocked(ImageboardError):
    def __init__(self):
        self.message = 'Board is locked'.format()
        super().__init__(self.message)


class ThreadNotFound(ImageboardError):
    def __init__(self):
        self.message = 'Thread not found'.format()
        super().__init__(self.message)


class ThreadIsLocked(ImageboardError):
    def __init__(self):
        self.message = 'Thread is locked'.format()
        super().__init__(self.message)


class BadMessageContent(ImageboardError):
    def __init__(self, reason):
        self.message = 'Bad message content: {reason}'.format(reason=reason)
        super().__init__(self.message)


class BadParameter(ImageboardError):
    def __init__(self, name):
        self.message = 'Parameter "{name}" is missing or has wrong value'.format(name=name)
        super().__init__(self.message)


class BadRequestType(ImageboardError):
    def __init__(self):
        self.message = 'Request should have POST type'.format()
        super().__init__(self.message)


class FormValidationError(ImageboardError):
    def __init__(self, data):
        self.message = 'Form is invalid'.format()
        self.data = data
        super().__init__(self.message)


class PostLimitWasReached(ImageboardError):
    def __init__(self):
        self.message = 'Post limit was reached'.format()
        super().__init__(self.message)
