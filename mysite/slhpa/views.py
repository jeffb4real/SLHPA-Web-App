import csv
import time
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.template import loader
from django.views import generic
from django.db.models import F
from .models import PhotoRecord

def index(request):

    photo_list = PhotoRecord.objects.order_by(F('year').asc(nulls_last=True))

    stats = {}
    stats['total'] = len(photo_list)

    query = request.GET.get('q')
    if query:
        reduced_list = []
        for photo in photo_list:
            if query in photo.title or query in photo.description:
                reduced_list.append(photo)
        photo_list = reduced_list

    stats['filtered'] = len(photo_list)
    photo_list = photo_list[0:10]
    stats['displayed'] = len(photo_list)
    template = loader.get_template('slhpa/index.html')
    context = {
        'photo_list': photo_list,
        'stats' : stats,
    }
    return HttpResponse(template.render(context, request))


def getField(row, fieldName):
    if row.get(fieldName):
        return row[fieldName]
    return ''


@transaction.atomic
def loaddb(request, db_filename):
    """
    csv file must be at root, e.g., <repo>/mysite/<file>, not in specific app directory.
    Example message seen in browser:
    Added 2526 records from C:\\Users\\chris\\Documents\\Github\\SLHPA-Web-App\\mysite/transformed.csv, exceptions: 0, no_resource: 4, no_key: 0, rows_in_table: 2526, seconds: 1
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
    return HttpResponse('Added ' + str(added) +
                ' records from ' + path_to_db +
                ', exceptions: ' + str(exceptions) +
                ', no_resource: ' + str(no_resource) +
                ', no_key: ' + str(no_key) +
                ', rows_in_table: ' + str(rows_in_table) +
                ', seconds: ' + str(int(end - start)))
