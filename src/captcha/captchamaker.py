import random
import base64
import io
import hashlib
import os

import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps

from captcha.wakabawords import make_word


COLOR_MODE = 'L'
BACKGROUND_COLOR = '#FFF'
MAIN_COLOR = '#000'

FONT_SIZE = 30
SYMBOL_SPACING = -5
SYMBOL_WIDTH = 15  # If Ubuntu font size 30
SYMBOL_HEIGHT = 30  # If Ubuntu font size 30
Y_DEVIATION = 2


# Load font object
module_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(module_dir, 'UbuntuMono-R.ttf'), 'rb') as f:
    font = PIL.ImageFont.truetype(font=f, size=FONT_SIZE)


def draw_distored_text(surface, text, left, top):
    x = left
    for char in text:
        y = random.randint(top - Y_DEVIATION, top + Y_DEVIATION)
        surface.text(xy=(x, y), text=char, fill=MAIN_COLOR, font=font, )
        x += (SYMBOL_WIDTH + SYMBOL_SPACING)


def draw_test_sheet():
    image = PIL.Image.new(COLOR_MODE, (1920, 1080), BACKGROUND_COLOR)
    surface = PIL.ImageDraw.Draw(image)

    for x in range(10):
        for y in range(20):
            solution = make_word()
            draw_distored_text(surface, solution, x * 200, y * 50)

    image = image.filter(PIL.ImageFilter.SHARPEN)
    image = image.filter(PIL.ImageFilter.FIND_EDGES)
    image = PIL.ImageOps.invert(image)

    image.show()


def draw_single_captcha(image_size=(200, 40)):
    image = PIL.Image.new(COLOR_MODE, image_size, BACKGROUND_COLOR)
    surface = PIL.ImageDraw.Draw(image)

    solution = make_word()
    draw_distored_text(surface, solution, 10, 5)

    image = image.filter(PIL.ImageFilter.SHARPEN)
    image = image.filter(PIL.ImageFilter.FIND_EDGES)
    image = PIL.ImageOps.invert(image)

    return image, solution


def make_captcha_create_kwargs():
    image, solution = draw_single_captcha()
    bytes_virtual_file = io.BytesIO()
    image.save(bytes_virtual_file, format='PNG')
    image_bytes = bytes_virtual_file.getvalue()
    image_base64 = 'data:image/png;base64,' + base64.b64encode(image_bytes).decode('ascii')

    return {
        'public_id': hashlib.md5(image_bytes).hexdigest(),
        'solution': solution,
        'image': image_base64,
    }


if __name__ == '__main__':
    draw_test_sheet()
