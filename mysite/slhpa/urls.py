from django.urls import path

from . import views

urlpatterns = [
    path('', views.List.as_view(), name="index"),
    path('list_all', views.index, name='index_all'),
    path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('edit/<str:id>/', views.bound_form, name='edit'),
    path('add/', views.add, name='add'),
    path('compare/<str:resource_name>/', views.photo_compare, name='compare'),

    # 'import' is a reserved word, can't do views.import .
    path('import/<import_filename>', views.loaddb, name='loaddb'),
    path('export/<export_filename>', views.export, name='export'),
    path('data/<str:filename>', views.datafile, name='data_file'),
]
