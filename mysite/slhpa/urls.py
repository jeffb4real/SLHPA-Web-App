from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('<db_filename>', views.loaddb, name='loaddb'),
    path('export/<db_filename>', views.export, name='export'),
]
