import datetime    # Python's module

from django.db import models
from django.utils import timezone

# Create your models here --
# This model code gives Django a lot of information. With it, 
# Django is able to:
# Create a database schema (CREATE TABLE statements) for this app.
# Create a Python database-access API for accessing Question and Choice
# objects.
# ------------------------

# From:
# https://docs.djangoproject.com/en/2.1/intro/tutorial02/
#
# A model is the single, definitive source of truth about your data. 
# It contains the essential fields and behaviors of the data you’re 
# storing. Django follows the DRY Principle. The goal is to define 
# your data model in one place and automatically derive things from it.

# Each model (class) is a sublass of django.db.models.Model
class Question(models.Model):
    # Each model has a number of class variables,
    # each of which represents a database field in the model.
    #
    # See list of Django model data types: 
    # https://www.webforefront.com/django/modeldatatypesandvalidation.html
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # It’s important to add __str__() methods to your models, not only for your
    # own convenience when dealing with the interactive prompt, but also because
    # objects’ representations are used throughout Django’s automatically-generated
    # admin.
    def __str__(self):
        return self.question_text

    # A custom method
    # There is a bug here that we will later fix, in the new function 
    # definition below.
    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # https://docs.djangoproject.com/en/2.1/intro/tutorial05/
    # Fixing the bug
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    # A relationship is defined, using ForeignKey. That tells Django 
    # each Choice is related to a single Question.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # It’s important to add __str__() methods to your models, not only for your
    # own convenience when dealing with the interactive prompt, but also because
    # objects’ representations are used throughout Django’s automatically-generated
    # admin site.
    def __str__(self):
        return self.choice_text

class SensorData(models.Model):
    # This model helps us put data from .csv files into our database
    # TODO: update model to make unique time_of_event
    #
    # If you’d like to specify a custom primary key, just specify primary_key=True
    # on one of your fields. If Django sees you’ve explicitly set Field.primary_key,
    # it won’t add the automatic id column.
    # Each model requires exactly one field to have primary_key=True
    # (either explicitly declared or automatically added).
    time_of_event = models.DateTimeField('time-Of-Event', primary_key=True)

    # Django model types and validation:
    # https://www.webforefront.com/django/modeldatatypesandvalidation.html
    #
    # TODO: figure out how to import options
    # photon1 = options.SmallIntegerField()
    # photon2 = options.SmallIntegerField()
    # photon3 = options.SmallIntegerField()
    #
    # Assume that there's one sensor per Photon board
    # 
    # https://docs.djangoproject.com/en/2.1/ref/models/
    #  null: If True, Django will store empty values as NULL in the database. Default is False.
    #  blank: If True, the field is allowed to be blank. Default is False.
    photon1 = models.IntegerField(null=True, blank=True)
    photon2 = models.IntegerField(null=True, blank=True)
    photon3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.time_of_event)

