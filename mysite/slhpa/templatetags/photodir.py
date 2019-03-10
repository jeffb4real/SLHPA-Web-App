from django import template

register = template.Library()

@register.filter
def getdir(value):
    try:
        photo_number = int(value[0:8])
    except:
        # Handle bad records by specifying an out-of-bounds directory number.
        # Should only happen in development when a bad PhotoRecord has been added to database.
        return '999'
    return str(int(photo_number / 900) + 1)
