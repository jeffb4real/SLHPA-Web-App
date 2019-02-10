from django import forms
from .models import PhotoRecord


class EditPhotoMetadataForm(forms.ModelForm):
    class Meta:
        model = PhotoRecord
        fields = ('title', 'description')
