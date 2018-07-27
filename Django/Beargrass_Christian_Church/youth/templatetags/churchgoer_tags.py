import random

from django import template

register = template.Library()


@register.inclusion_tag('youth/churchgoer.html')
def churchgoer_avatar(team):
    return {'Church Goer': churchgoer, 'num': random.randint(0, 215)}
