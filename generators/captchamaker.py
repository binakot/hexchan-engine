import random
import base64
import io
import os
import json
import hashlib

import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFilter

NUM_OF_CAPTCHAS = 10
COLOR_MODE = 'RGBA'
IMAGE_SIZE = (200, 50)
TRANSPARENT_COLOR = '#FFF'
MAIN_COLOR = '#000'
FONT_SIZE = 50
TEXT_LENGTH = 8

TEXT_DOT_THRESHOLD = 30
BG_DOT_THRESHOLD = 80

# SYMBOLS = [
#     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z',
#     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
# ]
# Some confusing symbols removed from the list
SYMBOLS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z',
    '2', '3', '4', '5', '6', '7', '8', '9',
]
NUM_OF_LINES = 5
LINE_WIDTH = 1

# Load font object
with open('UbuntuMono-R.ttf', 'rb') as f:
    font = PIL.ImageFont.truetype(font=f, size=FONT_SIZE)


def make_captcha():
    # Generate random string
    solution = ''.join([random.choice(SYMBOLS) for _ in range(0, TEXT_LENGTH)])

    # Create new image
    image = PIL.Image.new(COLOR_MODE, IMAGE_SIZE, TRANSPARENT_COLOR)

    # Create new surface from image and drow random string on it
    surface = PIL.ImageDraw.Draw(image)
    surface.text(xy=(0, 0), text=solution, fill=MAIN_COLOR, font=font)

    # # Apply contour filter and create new surface from the result
    # image = image.filter(PIL.ImageFilter.CONTOUR)
    surface = PIL.ImageDraw.Draw(image)

    for x in range(IMAGE_SIZE[0]):
        for y in range(IMAGE_SIZE[1]):
            current_color = image.getpixel(xy=(x, y))
            color_index = current_color[0] + current_color[1] + current_color[2]
            if color_index < 10:
                color_to_fill_text_contour = MAIN_COLOR if random.randint(1, 100) > TEXT_DOT_THRESHOLD else TRANSPARENT_COLOR
                surface.point(xy=[(x, y)], fill=color_to_fill_text_contour)
            else:
                color_to_fill_bg = MAIN_COLOR if random.randint(1, 100) > BG_DOT_THRESHOLD else TRANSPARENT_COLOR
                surface.point(xy=[(x, y)], fill=color_to_fill_bg)

    # for n in range(NUM_OF_LINES):
    #     surface.line(
    #         xy=[
    #             random.randrange(0, IMAGE_SIZE[0]), 1,
    #             random.randrange(0, IMAGE_SIZE[0]), IMAGE_SIZE[1]
    #         ],
    #         fill=MAIN_COLOR,
    #         width=LINE_WIDTH,
    #     )
    #     surface.line(
    #         xy=[
    #             1, random.randrange(0, IMAGE_SIZE[1]),
    #             IMAGE_SIZE[0], random.randrange(0, IMAGE_SIZE[1]),
    #         ],
    #         fill=MAIN_COLOR,
    #         width=LINE_WIDTH,
    #     )

    return image, solution


def make_captcha_base64():
    image, solution = make_captcha()

    bytes_virtual_file = io.BytesIO()

    image.save(bytes_virtual_file, format='PNG')

    image_bytes = bytes_virtual_file.getvalue()

    image_base64 = 'data:image/png;base64,' + base64.b64encode(image_bytes).decode('ascii')

    return image_base64


def make_captcha_show():
    image, solution = make_captcha()
    image.show()


if __name__ == '__main__':
    module_dir = os.path.dirname(os.path.abspath(__file__))
    fixture_filename = os.path.join(module_dir, '..', 'src', 'captcha', 'fixtures', 'captchas.json')
    captchas = []
    for n in range(1, NUM_OF_CAPTCHAS + 1):
        image, solution = make_captcha()

        bytes_virtual_file = io.BytesIO()

        image.save(bytes_virtual_file, format='PNG')

        image_bytes = bytes_virtual_file.getvalue()

        image_base64 = 'data:image/png;base64,' + base64.b64encode(image_bytes).decode('ascii')

        captcha = {
            "model": "captcha.captcha",
            "pk": n,
            "fields": {
                "public_id": hashlib.md5(image_bytes).hexdigest(),
                "solution": solution,
                "image": image_base64,
            }
        }

        captchas.append(captcha)
        print(n)

    with open(fixture_filename, 'w') as captcha_file:
        print(fixture_filename)
        json.dump(captchas, captcha_file, indent=4, ensure_ascii=False)
