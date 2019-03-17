from django_filters import FilterSet

from .models import PhotoRecord


class PhotoFilter(FilterSet):
    class Meta:
        model = PhotoRecord

        fields = {"title": ["contains"],
                  "description": ["contains"],
                  "subject": ["contains"],
                  "year": ["exact"],
                  }
