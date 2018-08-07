SITE_NAME = 'HEXCHAN.ORG'

DATE_TIME_FORMAT = 'd.m.Y в H:i:s'

POSTS_PER_THREAD_PER_PAGE = 5
THREADS_PER_PAGE = 10

CAPTCHA_ENABLED = False

IMAGE_DIR = 'images'
IMAGE_EXTENSION = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif'}
IMAGE_CHUNK_SIZE = 1 * (1024 * 1024)  # 1 MiB
IMAGE_THUMB_SIZE = 200, 200

THUMB_DIR = 'thumbs'
THUMB_EXTENSION = 'png'

FILE_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']
FILE_MAX_SIZE = 1 * (1024 * 1024)  # 1 MiB
FILE_MAX_NUM = 4

THREAD_HID_FORMAT = '{hid:03x}'
THREAD_HID_REGEX = '[0-9a-f]{3}'
THREAD_FULL_HID_FORMAT = '0x{hid:03x}'

POST_HID_FORMAT = '{hid:03x}'
POST_HID_REGEX = '[0-9a-f]{3}'
POST_FULL_HID_FORMAT = '0x{hid:03x}'

IMAGE_HID_FORMAT = '0x{hid:08x}'
