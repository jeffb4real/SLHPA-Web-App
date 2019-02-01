from django.http import HttpResponse
from django.conf import settings
import csv
import time
from .models import PhotoRecord

def index(request):
    return HttpResponse("Hello, world. You're at the slhpa index.")


def getField(row, fieldName):
    if row.get(fieldName):
        return row[fieldName]
    return ''


def loaddb(request, db_filename):
    """
    File must be at root, e.g., <repo>/mysite/<file>, not in specific app directory.
    Takes a few minutes, e.g.:
    Added 2526 records from C:\\Users\\chris\\Documents\\Github\\SLHPA-Web-App\\mysite/transformed.csv, exceptions: 0, no_resource: 4, no_key: 0, rows_in_table: 2526, seconds: 266
    TODO: Why doesn't it complain when record is added twice?
    TODO: Add null=True to all appropriate fields?
    """
    start = time.time()
    path_to_db = settings.BASE_DIR + '/' + db_filename

    # https://stackoverflow.com/questions/39962977/how-to-import-csv-file-to-django-models
    with open(path_to_db) as csvfile:
        added = 0
        exceptions = 0
        no_resource = 0
        no_key = 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if not row.get('resource_name'):
                    no_resource = no_resource + 1
                else:
                    key = getField(row, 'resource_name').replace('.pdf', '')
                    if not key:
                        no_key = no_key + 1
                    else:
                        year = None
                        if row.get('year'):
                            year = int(getField(row, 'year'))
                        pr = PhotoRecord(getField(row, 'address'),
                                getField(row, 'contributor'),
                                getField(row, 'description'),
                                getField(row, 'geo_coord_original'),
                                getField(row, 'geo_coord_UTM'),
                                getField(row, 'period_date'),
                                key,
                                getField(row, 'subject'),
                                getField(row, 'title'),
                                getField(row, 'url_for_file'),
                                getField(row, 'verified_gps_coords'),
                                year,
                                )
                        pr.save()
                        added = added + 1
            except Exception as e2:
                print(str(e2))
                exceptions = exceptions + 1
        rows_in_table = PhotoRecord.objects.all().count()

    end = time.time()
    print(end - start)
    return HttpResponse('Added ' + str(added) +
                ' records from ' + path_to_db +
                ', exceptions: ' + str(exceptions) +
                ', no_resource: ' + str(no_resource) +
                ', no_key: ' + str(no_key) +
                ', rows_in_table: ' + str(rows_in_table) +
                ', seconds: ' + str(int(end - start)))
