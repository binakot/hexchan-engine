from django import template
from django.utils.safestring import mark_safe

from markup import parse


register = template.Library()


@register.simple_tag
def markup(text, board_hid, thread_hid, post_hid):

    rendered_text, metadata = parse(text, board_hid, thread_hid, post_hid)
    return mark_safe(rendered_text)
