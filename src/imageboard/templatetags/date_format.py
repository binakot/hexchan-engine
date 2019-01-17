from datetime import datetime

from django import template

from hexchan import config


register = template.Library()


@register.filter
def date_format(value):
    return value.strftime(config.DATE_TIME_FORMAT)
