from django import template
from datetime import datetime
from django.utils.dateparse import parse_datetime

register = template.Library()


# Not working
@register.filter(name='time_difference')
def time_difference(date1, date2, *args, **kwargs):
    test = kwargs['test']
    return date1 - test
