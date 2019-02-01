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

    # Keep as CharField instead of IntegerField to handle keys such as '000001a'
    resource_name = models.CharField(max_length=100, primary_key=True)
    subject = models.CharField(max_length=1000)
    title = models.CharField(max_length=200)
    url_for_file = models.CharField(max_length=500)
    verified_gps_coords = models.CharField(max_length=100)
    year = models.IntegerField(null=True)


    def __str__(self):
        return self.resource_name + " : " + self.title

