import csv
import os
import time
import re

from enum import Enum

from django.conf import settings
from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import loader
from django.urls import reverse
from django.views import generic
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableMixin

from .filters import PhotoFilter
from .forms import AddPhotoMetadataForm, EditPhotoMetadataForm, RecordsPerPageForm, SingleEditFieldForm
from .models import KeyValueRecord, PhotoRecord
from .tables import PhotoTable
from .templatetags.photodir import getdir


def can_edit(request):
    return settings.ALLOW_EDIT or request.user.is_authenticated


class List(SingleTableMixin):
    """
    This view is a class-based, filtered view, based on class-based-filtered in django-tables2 example app.
    """
    table_class = PhotoTable
    model = PhotoRecord
    template_name = "slhpa/bootstrap_template.html"

    # Custom vars (not part of django or django_tables2)
    records_per_page = 10

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = {}
        stats['total'] = PhotoRecord.objects.all().count()
        stats['filtered'] = self.get_filtered_count(context)
        stats['records_per_page'] = self.records_per_page
        context["stats"] = stats
        context["form"] = RecordsPerPageForm(initial={'records_per_page': str(self.records_per_page)})
        context["allow_edit"] = can_edit(self.request)
        return context

    # See: django_tables2/views.py -> class (SingleTableMixin)
    def get_table_pagination(self, table):
        if self.request.GET.get('records_per_page'):
            self.records_per_page = int(self.request.GET['records_per_page'])
        return {"per_page": self.records_per_page}

    def get_filtered_count(self, context):
        return 0

class FilterViewList(List, FilterView):
    filterset_class = PhotoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photorecord_list' ] = PhotoRecord.objects.all()
        return context

    def get_filtered_count(self, context):
        return len(context['photorecord_list'])

class SingleEditFieldList(List, generic.base.TemplateView):
    query_type = '1'
    search_term = ''
    year_range = ''

    def get_year_range_filter(self):
        y1 = 0
        y2 = 0
        if '-' in self.year_range:
            [ys1, ys2] = self.year_range.split('-')
            y1 = int(ys1)
            y2 = int(ys2)
        else:
            y1 = y2 = int(self.year_range)
        return PhotoRecord.objects.filter(
                        (Q(title__icontains = self.search_term) | 
                        Q(description__icontains = self.search_term) | 
                        Q(subject__icontains = self.search_term)) &
                        Q(year__range = [y1, y2]))

    def get_queryset(self):
        if self.query_type == '2':
            if (self.year_range):
                return self.get_year_range_filter()
            return PhotoRecord.objects.filter(
                        Q(title__icontains = self.search_term) | 
                        Q(description__icontains = self.search_term) | 
                        Q(subject__icontains = self.search_term))
        if self.query_type == '3':
            return PhotoRecord.objects.filter(
                        Q(resource_name__icontains = self.search_term))
        return PhotoRecord.objects.all()

    def get_single_field_edit_form(self):
        choice = '1'
        if self.query_type == '3':
            choice = '2'
        return SingleEditFieldForm(initial={'search_type': choice, 
                        'search_term' : self.search_term,
                        'year_range' : self.year_range})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["single_edit_field_form"] = self.get_single_field_edit_form()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('search_term'):
            self.search_term = request.GET.get('search_term')
        if request.GET.get('query_type'):
            self.query_type = request.GET.get('query_type')
        if request.GET.get('year_range'):
            self.year_range = request.GET.get('year_range')
        return render(request, self.template_name,
                context = self.get_context_data(**kwargs))

    def validate_years(self, years):
        if '-' in years:
            m = re.search('[0-9]{4}-[0-9]{4}', years)
            try:
                self.year_range = m.group(0)
            except:
                pass
        else:
            m = re.search('[0-9]{4}', years)
            try:
                self.year_range = m.group(0)
            except:
                pass

    def post(self, request, *args, **kwargs):
        form = SingleEditFieldForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['search_type']
            self.search_term = form.cleaned_data['search_term']
            self.validate_years(form.cleaned_data['year_range'])
            if choice == '1':
                self.query_type = '2'
            else:
                self.query_type = '3'
            return HttpResponseRedirect(
                '/slhpa/new/?search_term=' + self.search_term + 
                '&query_type=' + str(self.query_type) +
                '&year_range=' + self.year_range)
        else:
            return render(request, self.template_name,
                context = self.get_context_data(**kwargs))

    def get_filtered_count(self, context):
        return len(self.get_queryset())


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
    # A kludge to get newly uploaded photos visible in the list view.
    # There will be no Sirsi URL, but having a non-null value makes the photo visible.
    photo.url_for_file = photo.resource_name


def handle_uploaded_file(resource_name, f):
    dir = getdir(resource_name) + '/'
    path = settings.BASE_DIR + '/slhpa/static/slhpa/images/photos/' + dir
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + resource_name + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def edit(request, id):
    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")
    photo = get_object_or_404(PhotoRecord, resource_name=id)
    if request.method == 'POST':
        form = EditPhotoMetadataForm(request.POST)
        if form.is_valid():
            load_photo_record(photo, form)
            photo.save()
            # TODO : Make backup copy of old photo file?
            if request.FILES.get('document'):
                handle_uploaded_file(photo.resource_name,
                                     request.FILES['document'])
            return HttpResponseRedirect('/slhpa/detail/' + id + '/')
        else:
            form = EditPhotoMetadataForm(instance=photo)
            return render(request, 'slhpa/edit.html',
                        {'form': form, 'photorecord': photo})
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

    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")

    if request.method == 'POST':
        form = AddPhotoMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            photo = PhotoRecord()
            photo.resource_name = get_next_resource_name()
            load_photo_record(photo, form)
            photo.save()
            if request.FILES.get('document'):
                handle_uploaded_file(photo.resource_name,
                                     request.FILES['document'])
            return HttpResponseRedirect('/slhpa/detail/' + photo.resource_name + '/')
        else:
            form = AddPhotoMetadataForm()
            return render(request, 'slhpa/add.html', {'form': form})
    else:
        form = AddPhotoMetadataForm()
        return render(request, 'slhpa/add.html', {'form': form})


def delete(request, id):
    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")
    photo = get_object_or_404(PhotoRecord, resource_name=id)
    if not 'test' in photo.description:
        return HttpResponseNotFound("Cannot delete non-test record: " + id)
    photo.delete()
    return HttpResponseNotFound("Deleted: " + id)
    

class DetailView(generic.DetailView):
    model = PhotoRecord
    template_name = 'slhpa/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allow_edit"] = can_edit(self.request)
        return context


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
    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")
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

    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")

    start = time.time()
    path_to_file = settings.BASE_DIR + \
        '/slhpa/static/slhpa/data/' + export_filename + '.csv'
    fieldnames = ['resource_name', 'title', 'subject', 'description',
                  'contributor',
                  'period_date', 'url_for_file', 'geo_coord_UTM', 'verified_gps_coords',
                  'year', 'geo_coord_original', 'address']
    records_written = 0
    with open(path_to_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        photo_list = PhotoRecord.objects.order_by(F('resource_name'))
        for photo in photo_list:
            writer.writerow(to_dict(photo))
            records_written += 1
    end = time.time()
    return HttpResponse('Wrote: ' + str(records_written) + ' records to: ' + path_to_file + ', seconds: ' + str(int(end - start)))


def datafile(request, filename):
    """
    Put data file into minimal html and return it.
    """
    if not can_edit(request):
        return HttpResponseNotFound("Unavailable")

    path_to_file = settings.BASE_DIR + '/slhpa/static/slhpa/data/' + filename
    data = ''
    with open(path_to_file) as f:
        for line in f:
            data = data + line + '<br>'
    return HttpResponse(data)


def photo_compare(request, resource_name):
    """
    Show same photo at different resolutions.
    """
    photo = get_object_or_404(PhotoRecord, resource_name=resource_name)
    return render(request, 'slhpa/photo_compare.html', {'photo': photo, })

def help(request):
    return render(request, 'slhpa/help.html')

def help2(request):
    return render(request, 'slhpa/help2.html')
