from django import forms
from .models import PhotoRecord
from django.core.validators import MaxValueValidator, MinValueValidator


min_latitude = -122.2
max_latitude = -122.15
min_longitude = 37.5
max_longitude = 38.0


class RecordsPerPageForm(forms.Form):
    # https://stackoverflow.com/questions/8859504/django-form-dropdown-list-of-numbers
    per_page_choices = (
        ('10', '10'),
        ('25', '25'),
        ('50', '50'),
        ('100', '100'),
        ('All', '2526'),
    )
    forms.ChoiceField(choices=per_page_choices)


class EditPhotoMetadataForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 60}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    year = forms.IntegerField(required=False)
    gps_latitude = forms.FloatField(required=False,
                                    validators=[MinValueValidator(
                                        min_latitude), MaxValueValidator(max_latitude)],
                                    label='Latitude (' + str(max_latitude) + ' to ' + str(min_latitude) + ')')
    gps_longitude = forms.FloatField(required=False,
                                     validators=[MinValueValidator(
                                         min_longitude), MaxValueValidator(max_longitude)],
                                     label='Longitude (' + str(min_longitude) + ' to ' + str(max_longitude) + ')')
    address = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    contributor = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    period_date = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    subject = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    document = forms.FileField(required=False, label='Photo (*must* be jpg)')

    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year', 'gps_latitude', 'gps_longitude',
                  'address', 'contributor', 'period_date', 'subject', 'document')


class AddPhotoMetadataForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 60}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    year = forms.IntegerField(required=False)
    gps_latitude = forms.FloatField(required=False,
                                    validators=[MinValueValidator(
                                        min_latitude), MaxValueValidator(max_latitude)],
                                    label='Latitude (' + str(max_latitude) + ' to ' + str(min_latitude) + ')')
    gps_longitude = forms.FloatField(required=False,
                                     validators=[MinValueValidator(
                                         min_longitude), MaxValueValidator(max_longitude)],
                                     label='Longitude (' + str(min_longitude) + ' to ' + str(max_longitude) + ')')
    address = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    contributor = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    period_date = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    subject = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    document = forms.FileField(required=False, label='Photo (*must* be jpg)')

    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year', 'gps_latitude', 'gps_longitude',
                  'address', 'contributor', 'period_date', 'subject', 'document')
