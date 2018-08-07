from gensokyo import config


class ThreadHidConverter:
    regex = config.THREAD_HID_REGEX

    def to_python(self, value):
        return int(value, 16)

    def to_url(self, value):
        return config.THREAD_HID_FORMAT.format(hid=value)


class PostHidConverter:
    regex = config.POST_HID_REGEX

    def to_python(self, value):
        return int(value, 16)

    def to_url(self, value):
        return config.POST_HID_FORMAT.format(hid=value)
