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
    address = models.CharField(max_length=100, null=True)
    contributor = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=2000)

    # This is only used to make the form provide an upload button.
    document = models.FileField(null=True)

    geo_coord_original = models.CharField(max_length=100, null=True)
    geo_coord_UTM = models.CharField(max_length=100, null=True)
    period_date = models.CharField(max_length=100, null=True)

    # Keep as CharField instead of IntegerField to handle keys such as '000001a'
    resource_name = models.CharField(max_length=100, primary_key=True)
    subject = models.CharField(max_length=1000, null=True)
    title = models.CharField(max_length=200)
    url_for_file = models.CharField(max_length=500)
    verified_gps_coords = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)

    # This should show enough information in the debugger, admin console, etc.
    def __str__(self):
        return self.resource_name + " : " + self.title

class KeyValueRecord(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key + "=" + self.value
