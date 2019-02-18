# tutorial/views.py
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Person
from .tables import PersonTable


# First version:
# def people(request):
#     return render(request, 'tutorial/people.html', {'people': Person.objects.all()})


def people(request):
    """
    You will then need to instantiate and configure the table in the view, before adding it to the context.
    """
    table = PersonTable(Person.objects.all())

    # Using RequestConfig automatically pulls values from request.GET and updates the table accordingly. This enables data ordering and pagination.
    RequestConfig(request).configure(table)

    # Rather than passing a QuerySet to {% render_table %}, instead pass the table instance:
    return render(request, 'tutorial/people.html', {'table': table})
