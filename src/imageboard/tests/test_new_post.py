# Standard imports
import datetime

# Django imports
from django.test import TestCase
from django.test import Client

# App imports
from imageboard.models import Board, Thread, Post
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
        }

    def check_redirect(self, response):
        # Check for handled exceptions
        if response.status_code != 302:
            e = response.context.get('exception')
            self.assertEqual(e, None)

        # Check for correct redirect
        self.assertRedirects(response, '/t/0x000000/', status_code=302, target_status_code=200)

    def check_post_created(self):
        post = Post.objects.get(thread__board__hid='t', hid=0)
        self.assertNotEqual(post, None)
        self.assertEqual(post.title, self.base_post_content['title'])
        self.assertEqual(post.author, self.base_post_content['author'])
        self.assertEqual(post.email, self.base_post_content['email'])
        self.assertEqual(post.text, self.base_post_content['text'])
        self.assertEqual(post.password, self.base_post_content['password'])

    def test_new_post_with_text(self):
        post_data = self.base_post_content.copy()
        post_data.update({})
        response = self.client.post('/create/', post_data)

        self.check_redirect(response)
        self.check_post_created()

    def test_new_post_with_image(self):
        post_data = self.base_post_content.copy()
        post_data.update({})
        response = self.client.post('/create/', post_data)

        self.check_redirect(response)
        self.check_post_created()
        # TODO: check images

    def test_new_post_many_images(self):
        post_data = self.base_post_content.copy()
        post_data.update({})
        response = self.client.post('/create/', post_data)

        self.check_redirect(response)
        self.check_post_created()
        # TODO: check images

    def test_lock_thread_after_reaching_limit(self):
        # TODO
        pass

    def test_new_session_info(self):
        # TODO
        pass

    def test_refs(self):
        # TODO
        pass
