# Standard library imports
import json
from pathlib import Path
import random
import shutil

# Third party imports
import faker


# Init faker tool
# ==============================================================================
fake = faker.Faker('la')


# Constants
# ==============================================================================
BOARDS_NUM = 5
THREADS_NUM = 32
POSTS_NUM = 128
IMAGE_NUM_CHOICES = [
    (0.3, 0),
    (0.7, 1),
    (0.8, 2),
    (0.9, 3),
    (1.0, 4),
]
CAPTCHA_NUM = 1000
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# Paths
# ==============================================================================
module_path = Path(__file__).resolve()
module_dir = module_path.parent

# Fixture paths
fixture_dir = module_dir / '..' / 'src' / 'imageboard' / 'fixtures'
boards_filename = fixture_dir / 'boards.json'
threads_filename = fixture_dir / 'threads.json'
posts_filename = fixture_dir / 'posts.json'
images_filename = fixture_dir / 'images.json'

# Upload paths
dev_dir = module_dir / '..' / 'dev'
available_images_filename = dev_dir / 'upload_fakes' / 'images.json'
upload_dir = dev_dir / 'upload'
upload_fake_dir = dev_dir / 'upload_fakes'

# Create images dirs
upload_dir.mkdir(parents=True, exist_ok=True)
upload_fake_dir.mkdir(parents=True, exist_ok=True)


# Helpers
# ==============================================================================
def get_value_by_chance(choices):
    random_num = random.random()
    for choice in choices:
        threshold, value = choice
        if random_num <= threshold:
            return value


def get_random_date():
    return fake.date_time_this_year().strftime(DATE_FORMAT)


def save_json_to_file(data, path):
    with path.open(mode='w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_json_from_file(path):
    with path.open(mode='r') as f:
        data = json.load(f)
    return data


def reset_dirs():
    pass

# Generators
# ==============================================================================
def make_thread(bnum, tnum):
    cur_date = get_random_date()

    thread = {
        "model": "imageboard.thread",
        "pk": bnum * THREADS_NUM + tnum + 1,
        "fields": {
            "hid": tnum * POSTS_NUM,
            "board": bnum,
            "op": bnum * THREADS_NUM * POSTS_NUM + tnum * POSTS_NUM + 1,
            "is_sticky": fake.boolean(1),
            "is_locked": fake.boolean(5),
            "is_deleted": fake.boolean(5),
            "max_posts_num": 512,
            "last_post_hid": 127,
            "created_at": cur_date,
            "updated_at": cur_date,
        }
    }

    return thread


def make_post(bnum, tnum, pnum):
    cur_date = get_random_date()
    has_name = fake.boolean(10)
    is_op = (pnum == 0)

    text_random_value = random.randint(1, 10)
    if text_random_value <= 2:
        text = "\n\n".join(fake.paragraphs(nb=5))
    elif text_random_value <= 4:
        text = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)
    elif text_random_value <= 6:
        text = fake.text(max_nb_chars=1024)
    elif text_random_value <= 8:
        text = fake.sentence(nb_words=10, variable_nb_words=True)
    else:
        text = ""

    post = {
        "model": "imageboard.post",
        "pk": bnum * THREADS_NUM * POSTS_NUM + tnum * POSTS_NUM + pnum + 1,
        "fields": {
            "hid": tnum * POSTS_NUM + pnum,
            "thread": bnum * THREADS_NUM + tnum + 1,
            "created_at": cur_date,
            "updated_at": cur_date,
            "text": text,
            "title": fake.sentence(nb_words=5, variable_nb_words=True) if (
                        fake.boolean(20) or is_op) else "",
            "author": fake.user_name() if has_name else "",
            "email": fake.free_email() if has_name else "",
            "password": fake.password() if fake.boolean(80) else "",
            "is_op": is_op,
            "user_was_warned": fake.boolean(5),
            "user_was_banned": fake.boolean(1),
            "ip_address": fake.ipv4(),
            "created_by": None,
            "is_deleted": 0 if is_op else fake.boolean(5),
        }
    }

    return post


def make_image(bnum, tnum, pnum, inum, image_data):
    cur_date = get_random_date()

    image_path = 'images/0x{id:08x}.{ext}'.format(id=inum + 1, ext=image_data['extension'])
    image_thumb_path = 'thumbs/0x{id:08x}.{ext}'.format(id=inum + 1, ext='png')

    # Image data structure
    image = {
        "model": "imageboard.image",
        "pk": inum + 1,
        "fields": {
            "post": bnum * THREADS_NUM * POSTS_NUM + tnum * POSTS_NUM + pnum + 1,
            "original_name": image_data["original_name"],
            "mimetype": image_data["mimetype"],
            "created_at": cur_date,
            "size": image_data["size"],
            "width": image_data["width"],
            "height": image_data["height"],
            "is_spoiler": False,
            "is_deleted": fake.boolean(1),
            "checksum": fake.md5(raw_output=False),
            "thumb_width": image_data["thumb_width"],
            "thumb_height": image_data["thumb_height"],
        }
    }

    (upload_dir / image_path).symlink_to(
        upload_fake_dir / 'images' / image_data['original_name']
    )

    (upload_dir / image_thumb_path).symlink_to(
        upload_fake_dir / 'thumbs' / image_data['base_name']
    )

    return image


# Main
# ==============================================================================
if __name__ == '__main__':
    # Reset output dirs
    shutil.rmtree(str(upload_dir))
    (upload_dir / 'images').mkdir(parents=True)
    (upload_dir / 'thumbs').mkdir(parents=True)

    # Load initial data
    boards_data = load_json_from_file(boards_filename)
    available_images = load_json_from_file(available_images_filename)

    # Data lists
    threads = []
    posts = []
    images = []

    # Image id counter
    inum = 0

    for bnum in range(BOARDS_NUM):
        for tnum in range(THREADS_NUM):
            thread = make_thread(bnum, tnum)
            threads.append(thread)

            for pnum in range(POSTS_NUM):
                post = make_post(bnum, tnum, pnum)
                posts.append(post)

                images_num = get_value_by_chance(IMAGE_NUM_CHOICES)

                for image_num in range(images_num):
                    # Select random image
                    image_data = random.choice(available_images)

                    image = make_image(bnum, tnum, pnum, inum, image_data)
                    images.append(image)
                    inum += 1

    save_json_to_file(threads, threads_filename)
    save_json_to_file(posts, posts_filename)
    save_json_to_file(images, images_filename)
