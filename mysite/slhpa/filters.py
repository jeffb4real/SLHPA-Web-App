from django_filters import FilterSet

from .models import PhotoRecord


class PhotoFilter(FilterSet):
    class Meta:
        model = PhotoRecord
        # fields = {"title": ["exact", "contains"],
        #           "description": ["exact", "contains"],
        #           "year": ["exact"],
        #           }
        fields = {"title": ["contains"]}
