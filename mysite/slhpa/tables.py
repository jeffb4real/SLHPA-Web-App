import django_tables2 as tables
from django.utils.html import format_html
from .models import PhotoRecord
from .templatetags.photodir import getdir


class PhotoTable(tables.Table):
    """
    While simple, passing a QuerySet directly to {% render_table %} does not allow for any customization. For that, you must define a custom Table class (this one)
    """

    # Customize column names
    url_for_file = tables.Column(verbose_name="Photo")
    resource_name = tables.Column(verbose_name="Picture Identifier")

    # https://django-tables2.readthedocs.io/en/latest/pages/custom-data.html?highlight=bound_column
    # # Table.render_foo methods
    # To change how a column is rendered, define a render_foo method on the table for example: render_row_number() for a column named row_number. This approach is suitable if you have a one-off change that you do not want to use in multiple tables.
    # record – the entire record for the row from the table data
    # value – the value for the cell retrieved from the table data
    # column – the Column object
    # bound_column – the BoundColumn object
    # bound_row – the BoundRow object
    # table – alias for self
    #
    # https://django-tables2.readthedocs.io/en/latest/pages/custom-data.html?highlight=ImageColumn
    def render_url_for_file(self, record):
        photo_filename = record.resource_name
        dir = getdir(record.resource_name) + '/'
        return format_html('<a href="/static/slhpa/images/photos/' + dir + photo_filename + '.jpg" target="_blank">' +
                           '    <div>' +
                           '        <img id="main_img" src="/static/slhpa/images/photos/' + dir + photo_filename + '.jpg" width="100%" border="2">' +
                           '        <img id="overlay_img" src="/static/slhpa/images/photos/finger.png" width="20%">' +
                           '    </div>' +
                           '</a>'
                           )

    class Meta:
        # https://django-tables2.readthedocs.io/en/latest/pages/table-data.html?highlight=exclude
        # customize what fields to show or hide:
        # sequence – reorder columns
        # fields – specify model fields to include
        # exclude – specify model fields to exclude
        model = PhotoRecord
        sequence = ('resource_name', 'title',
                    'description', 'year', 'url_for_file', '...')
        exclude = ('address', 'contributor', 'geo_coord_original',
                   'geo_coord_UTM', 'period_date', 'subject', 'verified_gps_coords',
                   'gps_latitude', 'gps_longitude')
        template_name = 'django_tables2/bootstrap.html'
