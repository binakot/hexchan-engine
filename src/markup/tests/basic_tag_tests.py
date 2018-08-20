from django.test import TestCase

from markup import wakaba


class WakabaBasicTagsTest(TestCase):
    def _get_url_by_hid(self, hid: str) -> str:
        return 'http://example.com/#{0}'.format(hid)

    def test_basic_em(self):
        self.assertEqual(
            wakaba.make_em_tags('*nomad*'),
            '<em>nomad</em>'
        )
        self.assertEqual(
            wakaba.make_em_tags('_nomad_'),
            '<em>nomad</em>'
        )

    def test_basic_strong(self):
        self.assertEqual(
            wakaba.make_strong_tags('**nomad**'),
            '<strong>nomad</strong>'
        )
        self.assertEqual(
            wakaba.make_strong_tags('__nomad__'),
            '<strong>nomad</strong>'
        )

    def test_basic_strike(self):
        self.assertEqual(
            wakaba.make_strike_tags('--nomad--'),
            '<s>nomad</s>'
        )

    def test_basic_spoiler(self):
        self.assertEqual(
            wakaba.make_spoiler_tags('%%nomad%%'),
            '<span class="spoiler">nomad</span>'
        )

    def test_basic_ref(self):
        self.assertEqual(
            wakaba.make_ref_tags('>>0x100500', self._get_url_by_hid),
            '>>0x100500'
        )
        self.assertEqual(
            wakaba.make_ref_tags('&gt;&gt;0x100500', self._get_url_by_hid),
            '<a class="ref" href="http://example.com/#0x100500">&gt;&gt;0x100500</a>'
        )

    def test_basic_urls(self):
        self.assertEqual(
            wakaba.make_url_tags('Please visit http://example.com'),
            'Please visit <a href="http://example.com" rel="nofollow">http://example.com</a>'
        )
