from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list_view, name='list'),
    path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),
    path('edit/<str:id>/', views.bound_form, name='edit'),

    # 'import' is a reserved word, can't do views.import .
    path('import/<import_filename>', views.loaddb, name='loaddb'),
    path('export/<export_filename>', views.export, name='export'),
    path('data/<str:filename>', views.datafile, name='data_file'),
]
