# tutorial/views.py
from django.shortcuts import render

# Using RequestConfig automatically pulls values from request.GET and updates the table accordingly. This enables data ordering and pagination.
from django_tables2 import RequestConfig
from .models import Person
from .tables import PersonTable


# Create your views here.

# def people(request):
#     return render(request, 'tutorial/people.html', {'people': Person.objects.all()})


def people(request):
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tutorial/people.html', {'table': table})
