# Read from csv file (or stdin) and write to Google Maps
import csv
import datetime
import sys


def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)


def handle_record(lines, record):
    geo_coords = record['geo_coord_UTM']
    if geo_coords and len(geo_coords) > 0:
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) == 2:
            lines.append('  <Placemark>\n')
            lines.append('    <name>' + record['asset_name'].replace('&', 'and') + '</name>\n')
            description = record['title'].replace('&','and') + ' / ' + record['resource_name'] + ' / ' + record['geo_coord_original']
            if record.get('address'):
                description += ' / ' + record['address']
            lines.append('    <description>' + description + '</description>\n')
            lines.append('    <Point>\n')
            lines.append('    <coordinates>' + coords[0].strip() + ',' + coords[1].strip() + ',0' + '</coordinates>\n')
            lines.append('    </Point>\n')
            lines.append('  </Placemark>\n')
            return 1
        else:
            return 0
    else:
        return 0


def write_kml_file(added_records, lines, kml_file_index):
    lines.append('</Document>\n')
    lines.append('</kml>\n')
    fn = 'data/SLHPA' + str(kml_file_index) + '.kml'
    with open(fn, 'w+') as kml_file:
        kml_file.writelines(lines)
    log("{: >4d}".format(added_records) + ' written. ' + fn)


def transform_to_kml(input_stream):
    reader = csv.DictReader(input_stream, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    MAX_RECORDS_PER_KML = 400
    kml_file_index = 0
    total_records_processed = 0
    added_records = 0
    lines = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<kml xmlns="http://www.opengis.net/kml/2.2">\n', '<Document>\n']
    for record in reader:
        added_records += handle_record(lines, record)
        total_records_processed += 1
        if added_records == MAX_RECORDS_PER_KML:
            write_kml_file(added_records, lines, kml_file_index)
            kml_file_index += 1
            added_records = 0
            lines = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<kml xmlns="http://www.opengis.net/kml/2.2">\n', '<Document>\n']
    if added_records > 0:
        write_kml_file(added_records, lines, kml_file_index)
    log("{: >4d}".format(total_records_processed) + ' records processed')


def main():
    transform_to_kml(open('data/transformed.csv'))


if '__main__' == __name__:
    main()
