"""Regular expressions ported from Wakaba.

See wakabautils.pl file in Wakaba package.
Version 3.0.9 was used.

Synthax: http://wakaba.c3.cx/docs/docs.html#WakabaMark

TODO: document regular expressions
TODO: tests
TODO: move ref expression to app config

Missing features:
TODO: code
TODO: lists
"""

import re
from typing import Callable, Union, List, Tuple

from hexchan import config
from imageboard.models import Board, Thread, Post


def make_url_tags(line: str) -> str:
    """Find URLs in string and replace them with <a> tags."""
    return re.sub(
        r"""
            (
                (?:http://|https://|ftp://|mailto:|news:|irc:)
                [^\s<>()"]*?
                (?:\([^\s<>()"]*?\)[^\s<>()"]*?)*)
                ((?:\s|<|>|"|\.||\]|!|\?|,|&\#44;|&quot;)*
                (?:[\s<>()"]|$)
            )
        """,
        r'<a href="\1" rel="nofollow">\1</a>',
        line,
        flags=re.X
    )


def make_em_tags(line: str) -> str:
    """Find emphasis marks in string and replace them with <em> tags."""
    return re.sub(
        r"""
            (?<![\w*]) 
            (\*|_) 
            (?![<>\s*_]) 
            ([^<>]+?) 
            (?<![<>\s*_]) 
            \1 (?![\w*]) 
        """,
        r'<em>\2</em>',
        line,
        flags=re.X
    )


def make_strong_tags(line: str) -> str:
    """Find strong marks in string and replace them with <strong> tags."""
    return re.sub(
        r"""
            (?<![\w*_]) 
            (\*\*|__) 
            (?![<>\s\*_]) 
            ([^<>]+?) 
            (?<![<>\s*_]) 
            \1 
            (?![\w*_])
        """,
        r'<strong>\2</strong>',
        line,
        flags=re.X
    )


def make_spoiler_tags(line: str) -> str:
    """Find spoiler marks in string and replace them with <span class="spoiler"> tags."""
    return re.sub(
        r"""
            (?<![\w%]) 
            (%%) 
            (?![<>\s%]) 
            ([^<>]+?) 
            (?<![<>\s%]) 
            \1 
            (?![\w%])
        """,
        r'<span class="spoiler">\2</span>',
        line,
        flags=re.X
    )


def make_strike_tags(line: str) -> str:
    """Find strike marks in string and replace them with <s> tags."""
    return re.sub(
        r"""
            (?<![\w-]) 
            (--) 
            (?![<>\s-]) 
            ([^<>]+?) 
            (?<![<>\s-]) 
            \1 
            (?![\w-])
        """,
        r'<s>\2</s>',
        line,
        flags=re.X
    )


def make_ref_tags(line: str, ref_url_getter: Callable) -> str:
    """Find post refs and replace them with links to those posts."""

    search_expression = re.compile(
        r'&gt;&gt;({})'.format(config.POST_HID_REGEX)
    )

    def replacement_function(matchobj):
        hid = matchobj.group(1)
        url = ref_url_getter(hid)

        if url is not None:
            return '<a class="ref js-ref" href="{url}">&gt;&gt;{hid}</a>'.format(url=url, hid=hid)
        else:
            return '<span class="dead_ref">&gt;&gt;{hid}</span>'.format(hid=hid)

    return search_expression.sub(replacement_function, line)


def make_all_inline_tags(text_line: str, ref_url_getter=None, make_links=True) -> str:
    """Make all inline tags, one after another."""

    if make_links:
        text_line = make_url_tags(text_line)
    text_line = make_strong_tags(text_line)
    text_line = make_em_tags(text_line)
    text_line = make_strike_tags(text_line)
    text_line = make_spoiler_tags(text_line)
    text_line = make_ref_tags(text_line, ref_url_getter=ref_url_getter)
    return text_line


def parse_text(text: str, board, thread, post, make_refs=True, make_links=True) -> str:
    """Make all text blocks with inline tags."""

    refs_dict = {ref.hid: ref for ref in post.refs.all()} if make_refs else {}

    def get_ref_url(hid: str) -> str:
        hid_int = int(hid, 16)
        referenced_post = refs_dict.get(hid_int)

        if make_refs and referenced_post:
            return referenced_post.get_absolute_url()
        else:
            return None

    html_lines = []

    text_lines = re.split('\n', text)
    for line in text_lines:
        # Skip empty lines
        if re.match(r'^\s*$', line):
            continue

        # Make quote tags
        elif re.match(r'^&gt;', line):
            html_line = '<blockquote>{line}</blockquote>'.format(
                line=make_all_inline_tags(line, ref_url_getter=get_ref_url, make_links=make_links)
            )

        # Make paragraphs for other cases
        else:
            html_line = '<p>{line}</p>'.format(
                line=make_all_inline_tags(line, ref_url_getter=get_ref_url, make_links=make_links)
            )

        if html_line:
            html_lines.append(html_line)

    full_text = '\n'.join(html_lines)

    return full_text


def extract_refs(text: str) -> list:
    """Extract post refs from text."""

    search_expression = re.compile(
        r'&gt;&gt;({})'.format(config.POST_HID_REGEX)
    )

    hex_hids = search_expression.findall(text)

    int_hids = [int(hid, 16) for hid in hex_hids]

    return int_hids
