from django import template
import markdown as md


register = template.Library()


@register.filter
def markdown(text):
    text = md.markdown(text)
    return text
