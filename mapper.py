# Read from csv file (or stdin) and write to Google Maps
import csv
import datetime
import sys
import re

# To make it easier to pretty print the XML, use lxml instead of ElementTree.
# "c:\Program Files\Python37\python.exe" -m pip install -U pip wheel setuptools
# pip install lxml
from lxml import etree

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)

class Mapper:
    max_name_length = 0
    max_desc_length = 0

    def has_year(self, record):
        pattern = r'\b(\d\d\d\d)\b'
        list_of_years = []
        list_of_years.extend(re.findall(pattern, record['title']))
        for year_str in list_of_years:
            year = int(year_str)
            if year >= 1800 and year <= 2019:
                return True
        return False

    def add_year_if_possible(self, record):
        if not self.has_year(record):
            year = record.get('year')
            if year:
                record['title'] += ', ' + year

    def handle_record(self, document_el, record, column_name):
        geo_coords = record.get(column_name)
        if not geo_coords or len(geo_coords) == 0:
            return 0
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) < 2:
            return 0
        self.add_year_if_possible(record)
        placemark = etree.SubElement(document_el, 'Placemark')
        name_element = etree.SubElement(placemark, 'name')
        name_element.text = record['title'] + ' [' + record['url_for_file'] + ']' 
        self.max_name_length = max(self.max_name_length, len(name_element.text))

        desc_element = etree.SubElement(placemark, 'description')
        desc_element.text = '[' + record['resource_name'].replace('.pdf', '') + '] '
        desc_element.text += record['description']
        desc_element.text += ' [' + record['geo_coord_original'] + ']'
        self.max_desc_length = max(self.max_desc_length, len(desc_element.text))

        point_element = etree.SubElement(placemark, 'Point')
        coords_element = etree.SubElement(point_element, 'coordinates')
        coords_element.text = coords[0].strip() + ',' + coords[1].strip() + ',0'
        return 1

    def write_kml_file(self, added_records, root, kml_file_index, filename_prefix):
        fn = 'data/' + filename_prefix + '_SLHPA_' + str(kml_file_index) + '.kml'
        with open(fn, 'w+') as kml_file:
            kml_file.writelines('<?xml version="1.0" encoding="UTF-8"?>\n')
            bytes = etree.tostring(root, pretty_print=True)
            kml_file.write(bytes.decode("utf-8"))
        log("{: >4d}".format(added_records) + ' records written to ' + fn)

    def master_coords_column_name(self, record):
        if record.get('verified_gps_coords'):
            return 'verified_gps_coords'
        return 'geo_coord_UTM'

    def calced_coords_column_name(self, record):
        return 'geo_coord_UTM'

    def manual_coords_column_name(self, record):
        return 'verified_gps_coords'

    def transform_to_kml(self, input_stream, filename_prefix, column_name_func):
        reader = csv.DictReader(input_stream, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        MAX_RECORDS_PER_KML = 2000
        kml_file_index = 0
        total_records_processed = 0
        added_records = 0
        root = etree.Element('kml')
        root.set('xmlns', 'http://www.opengis.net/kml/2.2')
        document = etree.SubElement(root, 'Document')
        for record in reader:
            # For the calculated reference GPS coordinate layer, only add GPS coords if there are verified geographic coords.
            if 'calced_ref' != filename_prefix or record.get('verified_gps_coords'):
                added_records += self.handle_record(document, record, column_name_func(record))
            total_records_processed += 1
            if added_records == MAX_RECORDS_PER_KML:
                self.write_kml_file(added_records, root, kml_file_index, filename_prefix)
                kml_file_index += 1
                added_records = 0
                root = etree.Element("kml")
        if added_records > 0:
            self.write_kml_file(added_records, root, kml_file_index, filename_prefix)
        return total_records_processed

    def main(self):
        self.transform_to_kml(open('data/transformed_no_rand.csv'), 'calced_no_rand', self.calced_coords_column_name)
        self.transform_to_kml(open('data/transformed.csv'), 'calced_ref', self.calced_coords_column_name)
        self.transform_to_kml(open('data/transformed.csv'), 'manual', self.manual_coords_column_name)

        self.max_name_length = 0
        self.max_desc_length = 0
        total_records_processed = self.transform_to_kml(open('data/transformed.csv'), 'calced', self.master_coords_column_name)
        log("{: >4d}".format(total_records_processed) + ' input records processed')
        log("{: >4d}".format(self.max_name_length) + ' max_name_length')
        log("{: >4d}".format(self.max_desc_length) + ' max_desc_length')

if '__main__' == __name__:
    Mapper().main()
