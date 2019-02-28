from django import template

register = template.Library()

@register.filter
def getdir(value):
    photo_number = int(value[0:8])
    return str(int(photo_number / 900) + 1)
