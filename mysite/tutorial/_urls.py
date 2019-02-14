# tutorial/urls.py
from django.conf.urls import url
from django.contrib import admin
from tutorial.views import people

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^people/', people),
]
