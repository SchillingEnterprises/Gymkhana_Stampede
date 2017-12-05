import markdown2
from django import template
from django.utils.safestring import mark_safe

from youth.models import ChurchGoer

register = template.Library()


@register.simple_tag
def newest_churchgoer():
    """Gets the most recent attendee that was added to the library"""
    return ChurchGoer.objects.latest('created_at')


@register.inclusion_tag('youth/churchgoer_nav.html')
def nav_youth_list():
    """Returns dictionary of attendees to display as navigation pane"""
    youth = ChurchGoer.objects.all()
    return {'youth': youth}


@register.filter('time_estimate')
def time_estimate(word_count):
    """Estimates the number of minutes it will take to complete a step based on the passed-in wordcount"""
    minutes = round(word_count / 20)
    return minutes


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    """Converts markdown text to HTML"""
    html_body = markdown2.markdown(markdown_text)
    return mark_safe(html_body)
