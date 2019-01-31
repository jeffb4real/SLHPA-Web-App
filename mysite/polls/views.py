# Create your views here.


# https://docs.djangoproject.com/en/2.1/intro/tutorial01/
# HttpResponseRedirect from tutorial04
from django.http import HttpResponse, HttpResponseRedirect

# https://docs.djangoproject.com/en/2.1/intro/tutorial03/
# tutorial04
from .models import Question, Choice

# Now no need to import loader (for our index function)
# because we're going to use render from django.shortcuts
#from django.template import loader

# It’s a very common idiom to load a template, fill a context and return
# an HttpResponse object with the result of the rendered template. Django
# provides a shortcut.
#from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

# tutorial03
from django.http import Http404

# tutorial04
from django.urls import reverse
from django.views import generic

# tutorial05
# Improving our view - also updated function get_queryset() below.
from django.utils import timezone

# Used for time.sleep()
import time
# To ingest .csv file
import csv
# Shell commands
import subprocess

# Playing with the API
# https://docs.djangoproject.com/en/2.1/intro/tutorial02/Playing with the API
from polls.models import SensorData


############################################
# tutorial04 - Using the generic view
# Next, we’re going to remove our old index, detail, and results views
# and use Django’s generic views instead.
#
# Our old vote() function, below, will still be used.
#
# We’re using two generic views here: ListView and DetailView. Respectively, those two
# views abstract the concepts of “display a list of objects” and “display a detail
# page for a particular type of object.”

# Each generic view needs to know what model it will be acting upon. This is
# provided using the model attribute.
# The DetailView generic view expects the primary key value captured from the
# URL to be called "pk", so we’ve changed question_id to pk for the generic views.

# Index is the list of questions
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # # tutorial04 - A class-based view, based on ListView:
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

    # tutorial05
    # The list of polls shows polls that aren’t published
    # yet (i.e. those that have a pub_date in the future).
    # We need to amend the get_queryset() method and change
    # it so that it also checks the date by comparing it with
    # Django's timezone.now().
    #
    # *NOTE*: Have to quit and re-run the Django server: $ python3 manage.py runserver
    # *NOTE*: New, filtered list of questions appears only at: http://localhost:8000/polls/
    #         The admin site (http://127.0.0.1:8000/admin/polls/question/) still has ALL
    #         the questions.
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    # tutorial05: Testing the DetailView
    # We're adding get_queryset() to remove future questions in the detail view,
    # similar to how we did to IndexView class above.
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    # tutorial01
    #return HttpResponse("You're voting on question %s." % question_id)

    # tutorial04
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice, dum-dum.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def loaddb(request, DBfilename):
    # Brute force - tell me what directory I'm in!! And make a full path to DB.
    #p = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
    #PathToDB = p.communicate()[0].rstrip().decode("utf-8") + '/polls/' + PathToDB
    #return HttpResponse("Here's the full path to PathToDB: %s" % PathToDB)

    # Hard-code a full path to DBfilename
    PathToDB = '/Users/urieow/mygithub/ovensensorweb/mysite/polls/' + DBfilename

    # How to import csv into Django model
    # https://stackoverflow.com/questions/39962977/how-to-import-csv-file-to-django-models
    with open(PathToDB) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # The header row values become your keys
            toe = row['time-Of-Event'].replace('/', '-')
            t1 = t2 = t3 = None
            if (row['thermistor-test']):
                t1 = row['thermistor-test']
            if (row['thermistor2-test']):
                t2 = row['thermistor2-test']
            if (row['thermistor3-test']):
                t3 = row['thermistor3-test']
            q = SensorData(toe, t1, t2, t3)
            q.save()
    return HttpResponse("Done reading " + PathToDB)


# ############################################
# # tutorial01
# def index(request):
#     return HttpResponse("Hellow world - you're at the polls index. Bruh.")

# # tutorial03
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# # tutorial03
# # Update our index view to use the polls/templates/polls/index.html template.
# # That code loads the template called polls/index.html and passes it a context.
# # The context is a dictionary mapping template variable names to Python objects.
# # Load the page by pointing your browser at “/polls/”, and you should see a
# # bulleted-list containing the “What’s up” question from Tutorial 2.
# # The link points to the question’s detail page.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# # No longer need to import loader because we're going to use Django's render instead.
# # (see comment above near the import)
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     # The render() function takes the request object as its first argument,
#     # a template name as its second argument and a dictionary as its optional
#     # third argument.
#     # It returns an HttpResponse object of the given template rendered with
#     # the given context.
#     return render(request, 'polls/index.html', context)

# ############################################

# # https://docs.djangoproject.com/en/2.1/intro/tutorial03/
# #
# # view - In Django, web pages and other content are delivered by views.
# # Each view is represented by a simple Python function (or method, in the
# # case of class-based views). Django will choose a view by examining the URL
# # that’s requested (to be precise, the part of the URL after the domain name).
# # 
# # Now let’s add a few more views to polls/views.py.
# # These views are slightly different, because they take an argument

# # tutorial01
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# # tutorial03
# # Raising a 404 error
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         # This is our custom error message
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

# # tutorial03
# # It’s a very common idiom to use get() and raise Http404 if the object
# # doesn’t exist. Django provides a shortcut.
# def detail(request, question_id):
#     # Unlike our prior custom error message, this code returns an
#     # automatic error message, "No Question matches the given query."
#     # 
#     # The first argument to get_object_or_404 is a Django model, and is
#     # followed by an arbitrary number of keyword arguments, which it
#     # passses to the get() function of the model's manager.
#     # It raises Http404 if the object doesn't exist.
#     #
#     # Philosophy:
#     # Why do we use a helper function get_object_or_404() instead of
#     # automatically catching the ObjectDoesNotExist exceptions at a higher
#     # level, or having the model API raise Http404 instead of ObjectDoesNotExist?
#     # Because that would couple the model layer to the view layer.
#     # One of the foremost design goals of Django is to maintain loose coupling.
#     # Some controlled coupling is introduced in the django.shortcuts module.
#     #
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# ############################################

# def results(request, question_id):
#     # tutorial01 - no actual results displayed
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)

#     # tutorial04
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# ############################################
