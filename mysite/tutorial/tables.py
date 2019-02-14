# tutorial/tables.py
import django_tables2 as tables
from .models import Person

# While simple, passing a QuerySet directly to {% render_table %} does not allow for any customization. For that, you must define a custom Table class:


class PersonTable(tables.Table):
    class Meta:
        model = Person
        template_name = 'django_tables2/bootstrap.html'
