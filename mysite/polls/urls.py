# To call the view, we need to map it to a URL - and for this we need a URLconf.
# 
# To create a URLconf in the polls directory, create a file called urls.py,
# in the polls directory, aka the app directory.

from django.urls import path

from . import views


# **Note: we had to comment out all this old code because Django
# parser had a problem with it - due to updated (generic) views
# added in polls/views.py.
#
# # https://docs.djangoproject.com/en/2.1/intro/tutorial03/
# # Wire these new views (mysite/polls/views.py) into the polls.urls module 
# # by adding the following path() calls.
# #
# # E.g.
# # http://localhost:8000/polls/34/
# # will show:
# # You're looking at question 34.
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     #path('<int:question_id>/', views.detail, name='detail'),
#     # added 'specifics/' which becomes part of the URL
#     path('specifics/<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# # tutorial03
# # Namespacing URL names
# app_name = 'polls'
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# tutorial04 - Use generic views; less code is better.
app_name = 'polls'
# Note that the name of the matched pattern in the path strings of the
# second and third patterns has changed from <question_id> to <pk>.
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<DBfilename>', views.loaddb, name='loaddb'),
]

