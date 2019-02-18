# tutorial/tables.py
import django_tables2 as tables
from .models import Person


class PersonTable(tables.Table):
    """
    While simple, passing a QuerySet directly to {% render_table %} does not allow for any customization. For that, you must define a custom Table class (this one)
    """
    class Meta:
        model = Person
        template_name = 'django_tables2/bootstrap.html'
