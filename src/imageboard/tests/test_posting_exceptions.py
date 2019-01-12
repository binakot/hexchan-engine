# Django imports
from django.test import TestCase
from django.test import Client

# App imports
from imageboard.models import Board, Thread, Post
from captcha.models import Captcha
import imageboard.exceptions as i_ex


class PostingExceptionsTestCase(TestCase):
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

    def make_bad_request(self, post_content_mixin, exception):
        post_data = self.base_post_content.copy()
        post_data.update(post_content_mixin)
        response = self.client.post('/create/', post_data)

        # Error template will be used with 403 status code
        self.assertTemplateUsed(response, 'imageboard/posting_error_page.html')
        self.assertEqual(response.status_code, 403)

        # Get exception from context
        e = response.context.get('exception')
        self.assertIsInstance(e, exception)

    def test_form_validation(self):
        self.make_bad_request({'form_type': 'bad'}, i_ex.FormValidationError)
        self.make_bad_request({'board_id': 'bad'}, i_ex.FormValidationError)
        self.make_bad_request({'thread_id': 'bad'}, i_ex.FormValidationError)

    def test_board_not_found(self):
        self.make_bad_request({'board_id': '100500'}, i_ex.BoardNotFound)

    def test_thread_not_found(self):
        self.make_bad_request({'thread_id': '100500'}, i_ex.ThreadNotFound)
