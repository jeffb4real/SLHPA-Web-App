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

class Sorter:
    field_indices = {}
    field_names_dict = {}

    def read_from_stream_into_dict(self, file_name):
        dict = {}
        fieldnames = None
        with open(file_name, 'r', newline='') as infile:
            reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fieldnames = reader.fieldnames
            for record in reader:
                if not record.get('year'):
                    continue
                if not record.get('geo_coord_original'):
                    continue
                key = record['geo_coord_original']
                if (len(key) < 4):
                    continue
                dict[record['resource_name']] = record
        log(str("{: >4d}".format(len(dict))) + ' records read from ' + file_name)
        return fieldnames, dict 

    def get_record_key(self, array_record):
        return array_record[self.field_indices['year']] + ' ' + array_record[self.field_indices['resource_name']]

    def to_array(self, dict_record):
        arr = []
        for key, value in dict_record.items():
            arr.insert(self.field_indices[key], value)
        return arr

    def to_dict(self, array_record):
        dict_record = {}
        i = 0
        for v in array_record:
            dict_record[self.field_names_dict[i]] = v
            i += 1
        return dict_record

    def do_sort(self, file_name):
        fieldnames, dict_records = self.read_from_stream_into_dict(file_name)
        i = 0
        for f in fieldnames:
            self.field_indices[f] = i
            self.field_names_dict[i] = f
            i += 1
        array_records = []
        for r in dict_records.values():
            array_records.append(self.to_array(r))
        return self.field_indices, sorted(array_records, key=self.get_record_key)

class Mapper:
    max_name_length = 0
    max_desc_length = 0
    max_name_record = 'unknown'
    max_desc_record = 'unknown'
    min_latitude = 1000.0
    max_latitude = -1000.0
    min_longitude = 1000.0
    max_longitude = -1000.0

    field_indices = {}

    def has_year(self, record):
        pattern = r'\b(\d\d\d\d)\b'
        list_of_years = []
        list_of_years.extend(re.findall(pattern, record[self.field_indices['title']]))
        for year_str in list_of_years:
            year = int(year_str)
            if year > 1838 and year < 2020:
                return True
        return False

    def add_year_if_possible(self, record):
        if not self.has_year(record):
            year = record[self.field_indices['year']]
            if year:
                record[self.field_indices['title']] += ', ' + year

    def handle_record(self, document_el, record, column_name):
        year = record[self.field_indices['year']]
        if not year or len(year) == 0:
            return 0
        geo_coords = record[self.field_indices[column_name]]
        if not geo_coords or len(geo_coords) == 0:
            return 0
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) < 2:
            return 0
        self.add_year_if_possible(record)
        placemark = etree.SubElement(document_el, 'Placemark')
        name_element = etree.SubElement(placemark, 'name')
        name_element.text = record[self.field_indices['title']] + ' [' + record[self.field_indices['url_for_file']] + ']' 
        if self.max_name_length < len(name_element.text):
            self.max_name_length = len(name_element.text)
            self.max_name_record = record[self.field_indices['resource_name']]

        desc_element = etree.SubElement(placemark, 'description')
        desc_element.text = '[' + record[self.field_indices['resource_name']].replace('.pdf', '') + '] '
        desc_element.text += record[self.field_indices['description']]
        desc_element.text += ' [' + record[self.field_indices['geo_coord_original']] + ']'
        if self.max_desc_length < len(desc_element.text):
            self.max_desc_length = len(desc_element.text)
            self.max_desc_record = record[self.field_indices['resource_name']]

        point_element = etree.SubElement(placemark, 'Point')
        coords_element = etree.SubElement(point_element, 'coordinates')
        coords_element.text = coords[0].strip() + ',' + coords[1].strip() + ',0'

        lat = float(coords[0])
        if lat > self.max_latitude:
            self.max_latitude = lat
        if lat < self.min_latitude:
            self.min_latitude = lat
        lon = float(coords[1])
        if lon > self.max_longitude:
            self.max_longitude = lon
        if lon < self.min_longitude:
            self.min_longitude = lon
        return 1

    data_dir = 'mysite/slhpa/static/slhpa/data/'
    def write_kml_file(self, added_records, root, kml_file_index, filename_prefix):
        fn = self.data_dir + filename_prefix + '_SLHPA_' + str(kml_file_index) + '.kml'
        with open(fn, 'w+') as kml_file:
            kml_file.writelines('<?xml version="1.0" encoding="UTF-8"?>\n')
            bytes = etree.tostring(root, pretty_print=True)
            kml_file.write(bytes.decode("utf-8"))
        log("{: >4d}".format(added_records) + ' records written to ' + fn)

    def master_coords_column_name(self, record):
        if record[self.field_indices['verified_gps_coords']]:
            return 'verified_gps_coords'
        return 'geo_coord_UTM'

    def calced_coords_column_name(self, record):
        return 'geo_coord_UTM'

    def manual_coords_column_name(self, record):
        return 'verified_gps_coords'

    def transform_to_kml(self, input_file_name, filename_prefix, column_name_func):
        self.field_indices, sorted_records = Sorter().do_sort(input_file_name)
        MAX_RECORDS_PER_KML = 2000
        kml_file_index = 0
        total_records_processed = 0
        added_records = 0
        root = etree.Element('kml')
        root.set('xmlns', 'http://www.opengis.net/kml/2.2')
        document = etree.SubElement(root, 'Document')
        for record in sorted_records:
            # For the calculated reference GPS coordinate layer, only add GPS coords if there are verified geographic coords.
            if 'calced_ref' != filename_prefix or record[self.field_indices['verified_gps_coords']]:
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
        self.transform_to_kml(self.data_dir + 'transformed_no_rand.csv', 'calced_no_rand', self.calced_coords_column_name)
        self.transform_to_kml(self.data_dir + 'transformed.csv', 'calced_ref', self.calced_coords_column_name)
        self.transform_to_kml(self.data_dir + 'transformed.csv', 'manual', self.manual_coords_column_name)

        self.max_name_length = 0
        self.max_desc_length = 0
        total_records_processed = self.transform_to_kml(self.data_dir + 'transformed.csv', 'calced', self.master_coords_column_name)
        log("{: >4d}".format(total_records_processed) + ' input records processed')
        log("{: >4d}".format(self.max_name_length) + ' max_name_length' + ' in ' + self.max_name_record)
        log("{: >4d}".format(self.max_desc_length) + ' max_desc_length' + ' in ' + self.max_desc_record)
        log("min_latitude: " + str(self.min_latitude) + ", max_latitude: " + str(self.max_latitude) + ", min_longitude: " + 
                str(self.min_longitude) + ", max_longitude: " + str(self.max_longitude))

if '__main__' == __name__:
    Mapper().main()
