import csv
import time
import os
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
from .models import PhotoRecord, KeyValueRecord
from .forms import EditPhotoMetadataForm, AddPhotoMetadataForm
from .tables import PhotoTable
from .templatetags.photodir import getdir
from django_tables2 import RequestConfig


def list_view(request):
    """
    You will then need to instantiate and configure the table in the view, before adding it to the context.
    """
    # table = PersonTable(Person.objects.all())
    # table = PhotoRecord.objects.order_by(F('year').asc(nulls_last=True))
    table = PhotoTable(PhotoRecord.objects.all())

    # Using RequestConfig automatically pulls values from request.GET and updates the table accordingly. This enables data ordering and pagination.
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

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
    # This will use index.html
    return HttpResponse(template.render(context, request))


def load_photo_record(photo, form):
    photo.title = form.cleaned_data['title']
    photo.description = form.cleaned_data['description']
    photo.year = form.cleaned_data['year']
    photo.gps_latitude = form.cleaned_data['gps_latitude']
    photo.gps_longitude = form.cleaned_data['gps_longitude']
    photo.address = form.cleaned_data['address']
    photo.contributor = form.cleaned_data['contributor']
    photo.period_date = form.cleaned_data['period_date']
    photo.subject = form.cleaned_data['subject']


def handle_uploaded_file(resource_name, f):
    dir = getdir(resource_name) + '/'
    path = settings.BASE_DIR + '/slhpa/static/slhpa/images/photos/' + dir 
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + resource_name + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def bound_form(request, id):
    photo = get_object_or_404(PhotoRecord, resource_name=id)
    if request.method == 'POST':
        form = EditPhotoMetadataForm(request.POST)
        if form.is_valid():
            load_photo_record(photo, form)
            photo.save()
            # TODO : Make backup copy of old photo file?
            if request.FILES.get('document'):
                handle_uploaded_file(photo.resource_name, request.FILES['document'])
        return HttpResponseRedirect('/slhpa/detail/' + id + '/')
    else:
        form = EditPhotoMetadataForm(instance=photo)
        return render(request, 'slhpa/edit.html',
                      {'form': form, 'photorecord': photo})


def add(request):
    def get_next_resource_name():
        kv = KeyValueRecord.objects.filter(key='next-resource-name')
        if kv:
            record = kv[0]
        else:
            # Yes, it's hardcoded. The old photo database will, however, never change.
            record = KeyValueRecord('next-resource-name', '00002557')
        current_name = record.value
        next_name = int(record.value)
        record.value = str("{:0>8d}".format(next_name + 1))
        record.save()
        return current_name

    if request.method == 'POST':
        form = AddPhotoMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            photo = PhotoRecord()
            photo.resource_name = get_next_resource_name()
            load_photo_record(photo, form)
            photo.save()
            if request.FILES.get('document'):
                handle_uploaded_file(photo.resource_name, request.FILES['document'])
            return HttpResponseRedirect('/slhpa/detail/' + photo.resource_name + '/')
    else:
        form = AddPhotoMetadataForm()
        return render(request, 'slhpa/add.html', {'form': form})


class DetailView(generic.DetailView):
    model = PhotoRecord
    template_name = 'slhpa/detail.html'


@transaction.atomic
def do_loaddb(request, import_filename):

    def getField(row, fieldName):
        if row.get(fieldName):
            return row[fieldName]
        return ''

    def load_gps(pr, source_string):
        vals = source_string.split(',')
        pr.gps_latitude = float(vals[1].replace(']', ''))
        pr.gps_longitude = float(vals[0].replace('[', ''))

    def load_record(row, key):
        pr = PhotoRecord()
        pr.address = getField(row, 'address')
        pr.contributor = getField(row, 'contributor')
        pr.description = getField(row, 'description')
        pr.geo_coord_original = getField(row, 'geo_coord_original')
        pr.geo_coord_UTM = getField(row, 'geo_coord_UTM')

        if row.get('verified_gps_coords'):
            load_gps(pr, getField(row, 'verified_gps_coords'))
        else:
            if row.get('geo_coord_UTM'):
                load_gps(pr, getField(row, 'geo_coord_UTM'))

        pr.period_date = getField(row, 'period_date')
        pr.resource_name = key
        pr.subject = getField(row, 'subject')
        pr.title = getField(row, 'title')
        pr.url_for_file = getField(row, 'url_for_file')
        pr.verified_gps_coords = getField(row, 'verified_gps_coords')
        year = None
        if row.get('year'):
            year = int(getField(row, 'year'))
        pr.year = year
        return pr

    start = time.time()
    path_to_db = settings.BASE_DIR + \
        '/slhpa/static/slhpa/data/' + import_filename + '.csv'

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
                        pr = load_record(row, key)
                        pr.save()
                        added = added + 1
            except Exception as e2:
                print(str(e2))
                exceptions = exceptions + 1

    end = time.time()
    return 'Added ' + str(added) + \
                        ' records from ' + path_to_db + \
                        ', exceptions: ' + str(exceptions) + \
                        ', no_resource: ' + str(no_resource) + \
                        ', no_key: ' + str(no_key) + \
                        ', seconds: ' + str(int(end - start))


def loaddb(request, import_filename):
    message = do_loaddb(request, import_filename)
    rows_in_table = PhotoRecord.objects.all().count()
    message = message + ', rows_in_table: ' + str(rows_in_table)
    return HttpResponse(message)


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
    path_to_file = settings.BASE_DIR + \
        '/slhpa/static/slhpa/data/' + export_filename + '.csv'
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


def datafile(request, filename):
    """
    Put data file into minimal html and return it.
    """
    path_to_file = settings.BASE_DIR + '/slhpa/static/slhpa/data/' + filename
    data = ''
    with open(path_to_file) as f:
        for line in f:
            data = data + line + '<br>'
    return HttpResponse(data)
