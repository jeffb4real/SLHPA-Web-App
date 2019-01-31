"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]


# The Django tutorial is a little unclear that 
# it's THIS urls.py (mysite-project/mysite/urls.py)
#
# https://docs.djangoproject.com/en/2.1/intro/tutorial01/
from django.contrib import admin
from django.urls import include, path

# The path() function is passed four arguments, 
# two required: route and view, and two optional: kwargs, and name.
#
# When somebody requests a page from your website – say, “/polls/34/”,
# Django will load the mysite/urls.py Python module because it’s pointed to
# by the ROOT_URLCONF setting.
# It finds the variable named urlpatterns and traverses the patterns in order. 
#
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]