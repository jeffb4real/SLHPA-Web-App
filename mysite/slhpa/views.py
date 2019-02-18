import csv
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db import transaction
from django.template import loader
from django.views import generic
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.urls import reverse
from .models import PhotoRecord
from .forms import EditPhotoMetadataForm

# For new 'list_view' view
from django_tables2 import RequestConfig
# from .models import Person    # replaced by 'from .models import PhotoRecord'
from .tables import PhotoTable


def list_view(request):
    """
    You will then need to instantiate and configure the table in the view, before adding it to the context.
    """
    # table = PersonTable(Person.objects.all())
    # table = PhotoRecord.objects.order_by(F('year').asc(nulls_last=True))
    table = PhotoTable(PhotoRecord.objects.all())

    # Using RequestConfig automatically pulls values from request.GET and updates the table accordingly. This enables data ordering and pagination.
    RequestConfig(request).configure(table)

    # Rather than passing a QuerySet to {% render_table %}, instead pass the table instance:
    return render(request, 'slhpa/list.html', {'table': table})


def index(request):

    photo_list = PhotoRecord.objects.order_by(F('year').asc(nulls_last=True))

    stats = {}
    stats['total'] = len(photo_list)

    query = request.GET.get('q')
    stats['query'] = query
    if query:
        reduced_list = []
        for photo in photo_list:
            if query in photo.title or query in photo.description:
                reduced_list.append(photo)
        photo_list = reduced_list

    stats['filtered'] = len(photo_list)
    stats['displayed'] = len(photo_list)
    template = loader.get_template('slhpa/index.html')
    context = {
        'photo_list': photo_list,
        'stats': stats,
    }
    return HttpResponse(template.render(context, request))


def bound_form(request, id):
    photo = get_object_or_404(PhotoRecord, resource_name=id)
    if request.method == 'POST':
        form = EditPhotoMetadataForm(request.POST)
        if form.is_valid():
            photo.title = form.cleaned_data['title']
            photo.description = form.cleaned_data['description']
            photo.year = form.cleaned_data['year']
            photo.verified_gps_coords = form.cleaned_data['verified_gps_coords']
            photo.address = form.cleaned_data['address']
            photo.contributor = form.cleaned_data['contributor']
            photo.period_date = form.cleaned_data['period_date']
            photo.subject = form.cleaned_data['subject']
            photo.save()
        return HttpResponseRedirect('/slhpa/detail/' + id + '/')
    else:
        form = EditPhotoMetadataForm(instance=photo)
        return render(request, 'slhpa/edit.html',
                      {'form': form, 'photorecord': photo})


class DetailView(generic.DetailView):
    model = PhotoRecord
    template_name = 'slhpa/detail.html'


@transaction.atomic
def loaddb(request, import_filename):

    def getField(row, fieldName):
        if row.get(fieldName):
            return row[fieldName]
        return ''

    """
    Example message seen in browser:
    Added 2526 records from C:\\Users\\chris\\Documents\\Github\\SLHPA-Web-App\\mysite/transformed.csv, exceptions: 0, no_resource: 4, no_key: 0, rows_in_table: 2526, seconds: 1
    TODO: Add null=True to all appropriate fields (for when new records are added).
    TODO: Why doesn't it complain when record is added twice with same key?
    """
    start = time.time()
    path_to_db = settings.BASE_DIR + '/../data/' + import_filename + '.csv'

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


def export(request, export_filename):

    def to_dict(photo_record):
        dict = {}
        dict['address'] = photo_record.address
        dict['contributor'] = photo_record.contributor
        dict['description'] = photo_record.description
        dict['geo_coord_original'] = photo_record.geo_coord_original
        dict['geo_coord_UTM'] = photo_record.geo_coord_UTM
        dict['period_date'] = photo_record.period_date
        dict['resource_name'] = photo_record.resource_name
        dict['subject'] = photo_record.subject
        dict['title'] = photo_record.title
        dict['url_for_file'] = photo_record.url_for_file
        dict['verified_gps_coords'] = photo_record.verified_gps_coords
        dict['year'] = photo_record.year
        return dict

    start = time.time()
    path_to_file = settings.BASE_DIR + '/../data/' + export_filename + '.csv'
    fieldnames = ['resource_name', 'title', 'subject', 'description',
                  'contributor',
                  'period_date', 'url_for_file', 'geo_coord_UTM', 'verified_gps_coords',
                  'year', 'geo_coord_original', 'address']
    with open(path_to_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        photo_list = PhotoRecord.objects.order_by(F('resource_name'))
        for photo in photo_list:
            writer.writerow(to_dict(photo))
    end = time.time()
    return HttpResponse('Wrote: ' + path_to_file + ', seconds: ' + str(int(end - start)))
