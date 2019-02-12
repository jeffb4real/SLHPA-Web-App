from django import forms
from .models import PhotoRecord


class EditPhotoMetadataForm(forms.ModelForm):

    year = forms.IntegerField(required=False)
    verified_gps_coords = forms.CharField(required=False)
    address = forms.CharField(required=False)
    contributor = forms.CharField(required=False)
    period_date = forms.CharField(required=False)
    subject = forms.CharField(required=False)

    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year', 'verified_gps_coords',
                    'address', 'contributor', 'period_date', 'subject')
