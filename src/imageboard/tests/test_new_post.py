# Standard imports
import os.path

# Django imports
from django.test import TestCase
from django.test import Client
from django.conf import settings

# App imports
from imageboard.models import Board, Thread, Post, Image
from captcha.models import Captcha


class NewPostTestCase(TestCase):
    def setUp(self):
        # Init testing client
        self.client = Client()

        # Create a board
        self.board = Board.objects.create(
            hid='t',
            name='testing',
            url='t',
            default_max_posts_num=100,
        )

        # Create a thread
        self.thread = Thread.objects.create(
            hid=0,
            board=self.board,
            max_posts_num=self.board.default_max_posts_num,
        )

        # Create a captcha
        Captcha.objects.create(
            public_id='100500',
            solution='swordfish',
            image='null',
        )

        # Update session with captcha info with this request
        self.client.get('/captcha/')

        # Base post content dict
        self.base_post_content = {
            'form_type': 'new_post',
            'board_id': '1',
            'thread_id': '1',
            'captcha_0': 'swordfish',
            'captcha_1': '100500',
            'title': 'Test title',
            'author': 'Tester',
            'email': '',
            'text': 'Test test test test',
            'password': 'swordfish',
            'images': [],
        }

        # Prepare upload dirs
        (settings.STORAGE_DIR / 'test').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'images').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'thumbs').mkdir(parents=True, exist_ok=True)

    def check_redirect(self, response, url):
        # Check for handled exceptions
        if response.status_code != 302:
            e = response.context.get('exception')
            self.assertEqual(e, None)

        # Check for correct redirect
        self.assertRedirects(response, url, status_code=302, target_status_code=200)

    def check_post_created(self, post_hid=0):
        post = Post.objects.get(thread__board__id=1, hid=post_hid)
        self.assertNotEqual(post, None)
        self.assertEqual(post.title, self.base_post_content['title'])
        self.assertEqual(post.author, self.base_post_content['author'])
        self.assertEqual(post.email, self.base_post_content['email'])
        self.assertEqual(post.text, self.base_post_content['text'])
        self.assertEqual(post.password, self.base_post_content['password'])

    def check_image_created(self, image_id, filename):
        image = Image.objects.get(id=image_id)
        self.assertNotEqual(image, None)
        self.assertEqual(image.original_name, os.path.basename(filename))

    def test_new_post_with_text(self):
        post_data = self.base_post_content.copy()
        post_data.update({})
        response = self.client.post('/create/', post_data)

        self.check_redirect(response, '/t/0x000000/')
        self.check_post_created()

    def test_new_post_with_image(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise.png')

        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                post_data = self.base_post_content.copy()
                post_data.update({'images': fp})
                response = self.client.post('/create/', post_data)

                self.check_redirect(response, '/t/0x000000/')
                self.check_post_created()
                self.check_image_created(1, filename)

    def test_new_post_many_images(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise.png')

        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp1, open(filename, 'rb') as fp2:
                post_data = self.base_post_content.copy()
                post_data.update({'images': [fp1, fp2]})
                response = self.client.post('/create/', post_data)

                self.check_redirect(response, '/t/0x000000/')
                self.check_post_created()
                self.check_image_created(1, filename)
                self.check_image_created(2, filename)

    def test_lock_thread_after_reaching_limit(self):
        little_thread = Thread.objects.create(
            hid=1,
            board=self.board,
            max_posts_num=1,
        )

        # First post should pass
        post_data = self.base_post_content.copy()
        post_data.update({'thread_id': '2'})
        response = self.client.post('/create/', post_data)
        self.check_redirect(response, '/t/0x000001/')

        little_thread_updated = Thread.objects.get(hid=1, board=self.board)
        self.assertEqual(little_thread_updated.is_locked, True)

    def test_new_session_info(self):
        # TODO
        pass

    def test_refs(self):
        # TODO
        pass
