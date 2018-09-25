import re
from typing import Tuple, Union

from django.urls import reverse

from markup import wakaba
from imageboard.models import Board, Thread, Post


quote_re = re.compile(r'^&gt;.*')
ref_re = re.compile(r'(&gt;&gt;0x[0-9a-f]{3}([0-9a-f]{3}))')
mini_ref_re = re.compile(r'(&gt;&gt;([0-9a-f]{3}))')


def parse(s, board_hid, thread_hid, post_hid):
    ref_base = '{url}#0x{thread_hid}'.format(
        url=reverse('thread_page', args=(board_hid, thread_hid)),
        thread_hid=format(thread_hid, '03x')
    )

    # Process initial string line by line
    html_lines = []
    for line in s.split('\n'):
        # Strip spaces
        line = line.strip()

        # Skip empty lines
        if line == '':
            continue

        # Find post refs
        line = ref_re.sub(r'<a class="ref" href="{ref_base}\g<2>">\g<1></a>'.format(ref_base=ref_base), line)

        # If line is a quoute wrap it with blockquote tag
        if quote_re.match(line):
            line = '<blockquote>{line}</blockquote>'.format(line=line)
        # If else make a paragraph
        else:
            line = '<p>{line}</p>'.format(line=line)

        # Add processed line to the list
        html_lines.append(line)

    # Join lines into single string
    html_string = '\n'.join(html_lines)

    # Refs data
    refs = [int(hid, 16) for (hid_with_brackets, hid) in ref_re.findall(s)]
    unique_refs = []
    for ref in refs:
        if ref not in unique_refs:
            unique_refs.append(ref)

    # Metadata
    metadata = {
        'refs': unique_refs
    }

    return html_string, metadata


def parse_post_text(text: str, board: Board, thread: Thread) -> Tuple[str, dict]:
    def make_url(hid):
        try:
            post = Post.objects.select(hid=hid, thread__board=Board)
            return post.get_absolute_url()
        except Post.DoesNotExist:
            return None

    parsed_text = wakaba.make_text_blocks(text)
    parsed_text_with_refs = wakaba.make_ref_tags(parsed_text, make_url)

