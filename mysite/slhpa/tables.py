import django_tables2 as tables
from django.utils.html import format_html
from .models import PhotoRecord


class PhotoTable(tables.Table):
    """
    While simple, passing a QuerySet directly to {% render_table %} does not allow for any customization. For that, you must define a custom Table class (this one)
    """

    # https://django-tables2.readthedocs.io/en/latest/pages/custom-data.html?highlight=bound_column
    # record – the entire record for the row from the table data
    # value – the value for the cell retrieved from the table data
    # column – the Column object
    # bound_column – the BoundColumn object
    # bound_row – the BoundRow object
    # table – alias for self

    # https://django-tables2.readthedocs.io/en/latest/pages/table-data.html?highlight=exclude
    # customize what fields to show or hide:
    # sequence – reorder columns
    # fields – specify model fields to include
    # exclude – specify model fields to exclude

    def render_url_for_file(self, value, record):
        url = record.url_for_file
        resource_name = record.resource_name

        # {% load static %}
        # {% static "/slhpa/images/photos" as baseUrl %}
        # <a href="{{ photo.url_for_file }}" target="_blank">
        #     <div>
        #         <img id="main_img" src="{{ baseUrl }}/{{ photo.resource_name }}.jpg" width="100%" border="2">
        #         <img id="overlay_img" src="{{ baseUrl }}/finger.png" width="20%">
        #     </div>
        # </a>
        return format_html('<a href="www.yahoo.com">yahoo</a>')

    class Meta:
        model = PhotoRecord
        sequence = ('resource_name', 'title',
                    'description', 'year', 'url_for_file', '...')
        exclude = ('address', 'contributor', 'geo_coord_original',
                   'geo_coord_UTM', 'period_date', 'subject', 'verified_gps_coords')
        template_name = 'django_tables2/bootstrap.html'

    # def get_top_pinned_data(self):
    #     """
    #     Pinned rows are not affected by sorting and pagination, they will be present on every page of the table, regardless of ordering. Values will be rendered just like you are used to for normal rows.
    #     """

    #     # first_name = tables.Column()
    #     # last_name = tables.Column()
    #     # Address Contributor Description Geo coord original  Geo coord UTM   Period date Resource name   Subject Title   Url for file    Verified gps coords Year
    #     return [
    #         {'first_name': 'Janet', 'last_name': 'Crossen'},
    #         # key 'last_name' is None here, so the default value will be rendered.
    #         {'first_name': 'Trine', 'last_name': None}
    #     ]
