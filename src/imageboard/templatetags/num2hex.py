from django import template

register = template.Library()


@register.filter
def num2hex(value):
    return format(value, '03x')
