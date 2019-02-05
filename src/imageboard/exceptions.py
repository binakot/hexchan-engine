from django.utils.translation import gettext_lazy as _

from hexchan import config
from imageboard.utils import get_pretty_file_size


class ImageboardError(Exception):
    pass


class BoardNotFound(ImageboardError):
    def __init__(self):
        self.message = _('Board not found')
        super().__init__(self.message)


class BoardIsLocked(ImageboardError):
    def __init__(self):
        self.message = _('Board is locked')
        super().__init__(self.message)


class ThreadNotFound(ImageboardError):
    def __init__(self):
        self.message = _('Thread not found')
        super().__init__(self.message)


class ThreadIsLocked(ImageboardError):
    def __init__(self):
        self.message = _('Thread is locked')
        super().__init__(self.message)


class BadMessageContent(ImageboardError):
    def __init__(self, reason='errors found'):
        self.message = _('Bad message content: {reason}').format(reason=reason)
        super().__init__(self.message)


class BadParameter(ImageboardError):
    def __init__(self, name):
        self.message = _('Parameter "{name}" is missing or has wrong value').format(name=name)
        super().__init__(self.message)


class BadRequestType(ImageboardError):
    def __init__(self):
        self.message = _('Request should have POST type')
        super().__init__(self.message)


class FormValidationError(ImageboardError):
    def __init__(self, data):
        self.message = _('Form is invalid')
        self.data = data
        super().__init__(self.message)


class PostLimitWasReached(ImageboardError):
    def __init__(self):
        self.message = _('Post limit was reached')
        super().__init__(self.message)


class MessageIsEmpty(ImageboardError):
    def __init__(self):
        self.message = _('Message should not be empty, either write some text or attach an image')
        super().__init__(self.message)


class TooManyFiles(ImageboardError):
    def __init__(self):
        self.message = _('Too many files attached, up to {max_files} file(s) are allowed').format(
            max_files=config.FILE_MAX_NUM
        )
        super().__init__(self.message)


class FileIsTooLarge(ImageboardError):
    def __init__(self):
        self.message = _('Attached file size is too large, sizes up to {file_size} are allowed').format(
            file_size=get_pretty_file_size(config.FILE_MAX_SIZE)
        )
        super().__init__(self.message)


class BadFileType(ImageboardError):
    def __init__(self):
        self.message = _('Attached file has an unsupported type, only types {types} are supported').format(
            types=', '.join(config.FILE_MIME_TYPES)
        )
        super().__init__(self.message)
