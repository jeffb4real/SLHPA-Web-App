from django import forms
from .models import PhotoRecord


class EditPhotoMetadataForm(forms.ModelForm):
    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year')

        # TODO : Unclear why these are requiring a value.
        # , 'verified_gps_coords', 'address', 'contributor', 'period_date', 'subject')
