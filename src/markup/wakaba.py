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


def make_url_tags(line: str) -> str:
    """Find URLs in string and replace them with <a> tags."""

    search_expression = re.compile(
        r"""
        (
            (?:http://|https://|ftp://|mailto:|news:|irc:)
            [^\s<>()"]*?
            (?:\([^\s<>()"]*?\)[^\s<>()"]*?)*)
            ((?:\s|<|>|"|\.||\]|!|\?|,|&\#44;|&quot;)*
            (?:[\s<>()"]|$)
        )
        """,
        re.X
    )

    replacement_expression = r'<a href="\1" rel="nofollow">\1</a>'

    return search_expression.sub(replacement_expression, line)


def make_em_tags(line: str) -> str:
    """Find emphasis marks in string and replace them with <em> tags."""

    search_expression = re.compile(
        r"""
            (?<![\w*]) 
            (\*|_) 
            (?![<>\s*_]) 
            ([^<>]+?) 
            (?<![<>\s*_]) 
            \1 (?![\w*]) 
        """,
        re.X
    )

    replacement_expression = r'<em>\2</em>'

    return search_expression.sub(replacement_expression, line)


def make_strong_tags(line: str) -> str:
    """Find strong marks in string and replace them with <strong> tags."""

    search_expression = re.compile(
        r"""
            (?<![\w*_]) 
            (\*\*|__) 
            (?![<>\s\*_]) 
            ([^<>]+?) 
            (?<![<>\s*_]) 
            \1 
            (?![\w*_])
        """,
        re.X
    )

    replacement_expression = r'<strong>\2</strong>'

    return search_expression.sub(replacement_expression, line)


def make_spoiler_tags(line: str) -> str:
    """Find spoiler marks in string and replace them with <span class="spoiler"> tags."""

    search_expression = re.compile(
        r"""
        (?<![\w%]) 
        (%%) 
        (?![<>\s%]) 
        ([^<>]+?) 
        (?<![<>\s%]) 
        \1 
        (?![\w%])
        """,
        re.X
    )

    replacement_expression = r'<span class="spoiler">\2</span>'

    return search_expression.sub(replacement_expression, line)


def make_strike_tags(line: str) -> str:
    """Find strike marks in string and replace them with <s> tags."""

    search_expression = re.compile(
        r"""
        (?<![\w-]) 
        (--) 
        (?![<>\s-]) 
        ([^<>]+?) 
        (?<![<>\s-]) 
        \1 
        (?![\w-])
        """,
        re.X
    )

    replacement_expression = r'<s>\2</s>'

    return search_expression.sub(replacement_expression, line)


def make_ref_tags(line: str, get_url_by_hid: Callable) -> str:
    """Find post refs and replace them with links to those posts."""

    search_expression = re.compile(r'&gt;&gt;(0x[0-9a-f]{6})')

    found_refs = []

    def replacement_function(matchobj):
        hid = matchobj.group(1)
        url = get_url_by_hid(int(hid, 16))

        if url is not None:
            return '<a class="ref" href="{url}">&gt;&gt;{hid}</a>'.format(url=url, hid=hid)
        else:
            return '<span class="dead_ref">&gt;&gt;{hid}</span>'.format(hid=hid)

    return search_expression.sub(replacement_function, line)


def make_all_inline_tags(text_line: str) -> str:
    """Make all inline tags, one after another."""

    text_line = make_url_tags(text_line)
    text_line = make_strong_tags(text_line)
    text_line = make_em_tags(text_line)
    text_line = make_strike_tags(text_line)
    text_line = make_spoiler_tags(text_line)
    return text_line


def make_text_blocks(text: str) -> str:
    """Make all text blocks with inline tags."""

    html_lines = []
    text_lines = re.split('\n', text)

    for line in text_lines:
        # Skip empty lines
        if re.match(r'^\s*$', line):
            continue

        # Make quote tags
        elif re.match(r'^&gt;', line):
            html_line = '<blockquote>{line}</blockquote>'.format(
                line=make_all_inline_tags(line)
            )

        # Make paragraphs for other cases
        else:
            html_line = '<p>{line}</p>'.format(
                line=make_all_inline_tags(line)
            )

        if html_line:
            html_lines.append(html_line)

    return '\n'.join(html_lines)

