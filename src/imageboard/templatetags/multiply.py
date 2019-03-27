from django import template


register = template.Library()


@register.filter
def multiply(value, multiplyier=1):
    return value * multiplyier
