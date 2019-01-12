from django.test import TestCase

from imageboard import wakabamark


class WakabaBasicTagsTest(TestCase):
    def _get_url_by_hid(self, hid: str) -> str:
        return 'http://example.com/#{0}'.format(hid)

    def _get_url_by_hid_empty(self, hid: str) -> None:
        return None

    def test_basic_em(self):
        self.assertEqual(
            wakabamark.make_em_tags('*nomad*'),
            '<em>nomad</em>'
        )
        self.assertEqual(
            wakabamark.make_em_tags('_nomad_'),
            '<em>nomad</em>'
        )

    def test_basic_strong(self):
        self.assertEqual(
            wakabamark.make_strong_tags('**nomad**'),
            '<strong>nomad</strong>'
        )
        self.assertEqual(
            wakabamark.make_strong_tags('__nomad__'),
            '<strong>nomad</strong>'
        )

    def test_basic_strike(self):
        self.assertEqual(
            wakabamark.make_strike_tags('--nomad--'),
            '<s>nomad</s>'
        )

    def test_basic_spoiler(self):
        self.assertEqual(
            wakabamark.make_spoiler_tags('%%nomad%%'),
            '<span class="spoiler">nomad</span>'
        )

    def test_basic_ref(self):
        self.assertEqual(
            wakabamark.make_ref_tags('>>0x100500', self._get_url_by_hid),
            '>>0x100500'
        )
        self.assertEqual(
            wakabamark.make_ref_tags('&gt;&gt;0x100500', self._get_url_by_hid),
            '<a class="ref js-ref" href="http://example.com/#0x100500">&gt;&gt;0x100500</a>'
        )
        self.assertEqual(
            wakabamark.make_ref_tags('&gt;&gt;0x100500', self._get_url_by_hid_empty),
            '<span class="dead_ref">&gt;&gt;0x100500</span>'
        )

    def test_basic_urls(self):
        self.assertEqual(
            wakabamark.make_url_tags('Please visit http://example.com'),
            'Please visit <a href="http://example.com" rel="nofollow">http://example.com</a>'
        )
