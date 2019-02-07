from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:photo_id>/', views.detail, name='detail'),
    path('<db_filename>', views.loaddb, name='loaddb'),
]
