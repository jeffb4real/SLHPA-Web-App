from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.List.as_view(), name="index"),
    path('list_all', views.index, name='index_all'),
    path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('edit/<str:id>/', views.bound_form, name='edit'),
    path('add/', views.add, name='add'),

    # 'import' is a reserved word, can't do views.import .
    path('import/<str:import_filename>', views.loaddb, name='loaddb'),
    path('export/<str:export_filename>', views.export, name='export'),
    path('data/<str:filename>', views.datafile, name='data_file'),
]

if settings.DEBUG:
    urlpatterns.append(path('compare/<str:resource_name>/', views.photo_compare, name='compare'))
