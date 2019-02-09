from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),

    # 'import' is a reserved word, can't do views.import .
    path('import/<import_filename>', views.loaddb, name='loaddb'),
    path('export/<export_filename>', views.export, name='export'),
]
