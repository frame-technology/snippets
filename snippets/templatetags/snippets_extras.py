from django import template
import datetime

register = template.Library()

@register.filter
def deltaDays(start_date, days=4):
    end_date = start_date + datetime.timedelta(days=days)
    return end_date
