from django import forms
from .models import PhotoRecord


class EditPhotoMetadataForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 60}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    year = forms.IntegerField(required=False)
    verified_gps_coords = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    address = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    contributor = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    period_date = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    subject = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))

    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year', 'verified_gps_coords',
                    'address', 'contributor', 'period_date', 'subject')

class AddPhotoMetadataForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 60}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    year = forms.IntegerField(required=False)
    verified_gps_coords = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    address = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    contributor = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    period_date = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    subject = forms.CharField(required=False, 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 60}))
    document = forms.FileField(required=False)

    class Meta:
        model = PhotoRecord
        fields = ('title', 'description', 'year', 'verified_gps_coords',
                    'address', 'contributor', 'period_date', 'subject', 'document')
