# tutorial/models.py
from django.db import models

# Create your models here.

# From:
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name='full name')
