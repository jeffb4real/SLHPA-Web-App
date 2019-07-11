from django.urls import path
from django.conf import settings
from django.db.utils import OperationalError

try:
    from . import views

    urlpatterns = [
        path('', views.List.as_view(), name="index"),
        path('detail/<str:pk>/', views.DetailView.as_view(), name='detail'),
        path('data/<str:filename>', views.datafile, name='data_file'),
        path('edit/<str:id>/', views.edit, name='edit'),
        path('delete/<str:id>/', views.delete, name='delete'),
        path('add/', views.add, name='add'),

        # 'import' is a reserved word, can't do views.import .
        path('import/<str:import_filename>', views.loaddb, name='loaddb'),
        path('export/<str:export_filename>', views.export, name='export'),
        path('compare/<str:resource_name>/', views.photo_compare, name='compare'),
        path('help', views.help, name='help'),
        path('help2', views.help2, name='help2'),
    ]
except OperationalError:
    # https://stackoverflow.com/questions/34548768/django-no-such-table-exception
    # happens when db doesn't exist yet, dummyview.py should be importable without this side effect
    from . import dummyview
    urlpatterns = [
        path('hello', dummyview.hello, name='hello'),
    ]
