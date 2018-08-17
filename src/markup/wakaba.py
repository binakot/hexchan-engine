"""Regular expressions ported from Wakaba.

See wakabautils.pl file in Wakaba package.
Version 3.0.9 was used.

Synthax: http://wakaba.c3.cx/docs/docs.html#WakabaMark

TODO: document regular expressions
TODO: code
TODO: lists
TODO: quotes
TODO: refs
"""

import re


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
            (?<![\w*]) 
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
        (?<![\w*]) 
        (%%) 
        (?![<>\s\*_]) 
        ([^<>]+?) 
        (?<![<>\s*_]) 
        \1 
        (?![\w*_])
        """,
        re.X
    )

    replacement_expression = r'<span class="spoiler">\2</span>'

    return search_expression.sub(replacement_expression, line)
