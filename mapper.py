# Read from csv file (or stdin) and write to Google Maps
import csv
import datetime
import sys

# To make it easier to pretty print the XML, use lxml instead of ElementTree.
# "c:\Program Files\Python37\python.exe" -m pip install -U pip wheel setuptools
# pip install lxml
from lxml import etree

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)

def handle_record(document_el, record, column_name):
    geo_coords = record[column_name]
    if geo_coords and len(geo_coords) > 0:
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) == 2:
            placemark = etree.SubElement(document_el, 'Placemark')
            name_element = etree.SubElement(placemark, 'name')
            name_element.text =  record['title'].replace('&', 'and')
            name_element.text += ' [' + record['url_for_file'] + ']' 

            desc_element = etree.SubElement(placemark, 'description')
            desc_element.text = record['description'].replace('&','and')
            desc_element.text += ' [' + record['resource_name'].replace('.pdf', '') + ']'

            point_element = etree.SubElement(placemark, 'Point')
            coords_element = etree.SubElement(point_element, 'coordinates')
            coords_element.text = coords[0].strip() + ',' + coords[1].strip() + ',0'
            return 1
        else:
            return 0
    else:
        return 0

def write_kml_file(added_records, root, kml_file_index, filename_prefix):
    fn = 'data/' + filename_prefix + '_SLHPA_' + str(kml_file_index) + '.kml'
    with open(fn, 'w+') as kml_file:
        kml_file.writelines('<?xml version="1.0" encoding="UTF-8"?>\n')
        bytes = etree.tostring(root, pretty_print=True)
        bytes.decode("utf-8").replace('\n','\r\n')
        kml_file.write(bytes.decode("utf-8"))
    log("{: >4d}".format(added_records) + ' records written to ' + fn)

def transform_to_kml(input_stream, filename_prefix, column_name):
    reader = csv.DictReader(input_stream, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    MAX_RECORDS_PER_KML = 400
    kml_file_index = 0
    total_records_processed = 0
    added_records = 0
    root = etree.Element('kml')
    root.set('xmlns', 'http://www.opengis.net/kml/2.2')
    document = etree.SubElement(root, 'Document')
    for record in reader:
        # For the calculated reference GPS coordinate layer, only add GPS coords if there are verified geographic coords.
        if 'calced_ref' != filename_prefix or record.get('verified_gps_coords'):
            added_records += handle_record(document, record, column_name)
        total_records_processed += 1
        if added_records == MAX_RECORDS_PER_KML:
            write_kml_file(added_records, root, kml_file_index, filename_prefix)
            kml_file_index += 1
            added_records = 0
            root = etree.Element("Document")
    if added_records > 0:
        write_kml_file(added_records, root, kml_file_index, filename_prefix)
    return total_records_processed

def main():
    transform_to_kml(open('data/transformed.csv'), 'calced', 'geo_coord_UTM')
    transform_to_kml(open('data/transformed.csv'), 'calced_ref', 'geo_coord_UTM')
    total_records_processed = transform_to_kml(open('data/transformed.csv'), 'manual', 'verified_gps_coords')
    log("{: >4d}".format(total_records_processed) + ' input records processed')

if '__main__' == __name__:
    main()
