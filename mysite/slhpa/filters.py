import django_filters as filters
from .models import PhotoRecord


class PhotoFilter(filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(PhotoFilter, self).__init__(*args, **kwargs)
        self.filters['resource_name__contains'].label = "Photo Identifier contains"

    class Meta:
        model = PhotoRecord
        fields = {
            "resource_name": ["contains"],
            "title": ["contains"],
            "description": ["contains"],
            "subject": ["contains"],
            "year": ["exact"],
        }
