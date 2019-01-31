from django.contrib import admin

#----
# Register your models here.
# https://docs.djangoproject.com/en/2.1/intro/tutorial02/

# Make the poll app modifiable in the admin:
# Our poll app isn't displayed on the admin index page.
# Just one thing to do: we need to tell the admin that Question objects
# have an admin interface.
from .models import Question
from .models import SensorData

admin.site.register(Question)
admin.site.register(SensorData)
