from django.db import models

#  column names from transformed.csv not included:
# asset_name
# description2
# digital_format
# file_size
# Index Number
# Notes
# paper_page_number
# resource_number
# source_index
# Title
# Volume

class PhotoRecord(models.Model):
    address = models.CharField(max_length=100)
    contributor = models.CharField(max_length=1000)
    description = models.CharField(max_length=2000)
    geo_coord_original = models.CharField(max_length=100)
    geo_coord_UTM = models.CharField(max_length=100)
    period_date = models.CharField(max_length=100)
    resource_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=1000)
    title = models.CharField(max_length=200)
    url_for_file = models.CharField(max_length=500)
    verified_gps_coords = models.CharField(max_length=100)
    year = models.IntegerField()
