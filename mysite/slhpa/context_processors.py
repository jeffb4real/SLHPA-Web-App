import django
def django_version(request):
    return { 'django_version': django.get_version() }