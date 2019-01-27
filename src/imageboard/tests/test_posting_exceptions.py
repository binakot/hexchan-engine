# Standard imports
import os.path
import datetime

# Django imports
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.utils import timezone

# App imports
from imageboard.models import Board, Thread, Post
import imageboard.exceptions as i_ex

from captcha.models import Captcha

from moderation.models import Ban, BanReason, ImageFilter, WordFilter
import moderation.exceptions as m_ex


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

        # Prepare upload dirs
        (settings.STORAGE_DIR / 'test').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'images').mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_DIR / 'test' / 'thumbs').mkdir(parents=True, exist_ok=True)

    def make_bad_request(self, post_content_mixin, exception, **extra_client_kwargs):
        post_data = self.base_post_content.copy()
        post_data.update(post_content_mixin)
        response = self.client.post('/create/', post_data, **extra_client_kwargs)

        # Error template will be used with 403 status code
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'imageboard/posting_error_page.html')

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

    def test_board_is_locked(self):
        locked_board = Board.objects.create(
            hid='b',
            name='random',
            url='b',
            default_max_posts_num=100,
            is_locked=True,
        )
        locked_thread = Thread.objects.create(
            hid=1,
            board=self.board,
            max_posts_num=1,
            is_locked=True,
        )
        self.make_bad_request({'board_id': '2', 'thread_id': '2'}, i_ex.BoardIsLocked)

    def test_thread_is_locked(self):
        locked_thread = Thread.objects.create(
            hid=1,
            board=self.board,
            max_posts_num=1,
            is_locked=True,
        )
        self.make_bad_request({'thread_id': '2'}, i_ex.ThreadIsLocked)

    def test_make_get_request(self):
        post_data = self.base_post_content.copy()
        response = self.client.get('/create/', post_data)

        # Error template will be used with 403 status code
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'imageboard/posting_error_page.html')

        # Get exception from context
        e = response.context.get('exception')
        self.assertIsInstance(e, i_ex.BadRequestType)

    def test_attached_non_image(self):
        filename = os.path.join(os.path.dirname(__file__), 'not_image.txt')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_request({'images': fp}, i_ex.BadFileType)

    def test_attached_large_image(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise_big.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_request({'images': fp}, i_ex.FileIsTooLarge)

    def test_attached_too_many_images(self):
        filename = os.path.join(os.path.dirname(__file__), 'noise.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp1, open(filename, 'rb') as fp2, open(filename, 'rb') as fp3, open(filename, 'rb') as fp4, open(filename, 'rb') as fp5, open(filename, 'rb') as fp6, open(filename, 'rb') as fp7, open(filename, 'rb') as fp8:
                self.make_bad_request({'images': [fp1, fp2, fp3, fp4, fp5, fp6, fp7, fp8]}, i_ex.TooManyFiles)

    def test_wordfilter(self):
        WordFilter.objects.create(expression='nomad')
        WordFilter.objects.create(expression='huita')
        self.make_bad_request({'text': 'nomad huita'}, m_ex.BadMessage)

    def test_advanced_wordfilter(self):
        WordFilter.objects.create(expression='^huit(a|ariy)')
        WordFilter.objects.create(expression='^nomad')
        self.make_bad_request({'text': 'huitariy'}, m_ex.BadMessage)
        self.make_bad_request({'text': 'nomadia'}, m_ex.BadMessage)

    def test_imagefilter(self):
        # Use noise.png
        ImageFilter.objects.create(checksum='023943b7771ab11604a64ca306cc0ec4', size='82633')

        filename = os.path.join(os.path.dirname(__file__), 'noise.png')
        with self.settings(MEDIA_ROOT=str(settings.STORAGE_DIR / 'test')):
            with open(filename, 'rb') as fp:
                self.make_bad_request({'images': fp}, m_ex.BadImage)

    def test_ban_ip(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_ip = '93.184.216.34'

        Ban.objects.create(type=Ban.BAN_TYPE_IP, value=banned_ip, reason=reason, active_until=tomorrow)

        self.make_bad_request({}, m_ex.Banned, REMOTE_ADDR=banned_ip)

    def test_ban_session(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_session = self.client.session.session_key

        Ban.objects.create(type=Ban.BAN_TYPE_SESSION, value=banned_session, reason=reason, active_until=tomorrow)

        self.make_bad_request({}, m_ex.Banned)

    def test_ban_network(self):
        reason = BanReason.objects.create(description='Trolling')

        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)

        banned_network = '93.184.216.0/24'
        banned_ip = '93.184.216.34'

        Ban.objects.create(type=Ban.BAN_TYPE_NET, value=banned_network, reason=reason, active_until=tomorrow)

        self.make_bad_request({}, m_ex.ModerationError, REMOTE_ADDR=banned_ip)
