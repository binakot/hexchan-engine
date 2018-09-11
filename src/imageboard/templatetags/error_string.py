from django import template

from imageboard.errors.strings import error_strings

register = template.Library()


@register.simple_tag
def error_string(error_code: str) -> str:
    return error_strings.get(error_code, 'Неизвестная ошибка')
