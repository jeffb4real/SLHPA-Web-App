# Read from csv file (or stdin) and write to Google Maps
import csv


def handle_record(lines, record):
    geo_coords = record['geo_coord_UTM']
    if geo_coords is not None and len(geo_coords) > 0:
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) == 2:
            lines.append('  <Placemark>\n')
            lines.append('    <name>' + record['asset_name'] + '</name>\n')
            lines.append('    <description>' + record['description'] + ' [' + record['resource_name'] + ']' + '</description>\n')
            lines.append('    <Point>\n')
            lines.append('    <coordinates>' + coords[1].strip() + ',' + coords[0].strip() + ',0' + '</coordinates>\n')
            lines.append('    </Point>\n')
            lines.append('  </Placemark>\n')
            return 1
        else:
            return 0
    else:
        return 0


def read_from_stream(input_stream):
    reader = csv.DictReader(input_stream, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    total_records = 0
    added_records = 0
    lines = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<kml xmlns="http://www.opengis.net/kml/2.2">\n', '<Document>\n']
    for record in reader:
        added_records += handle_record(lines, record)
        total_records += 1
    lines.append('</Document>\n')
    lines.append('</kml>\n')
    with open('data/SLHPA.kml', 'w+') as kml_file:
        kml_file.writelines(lines)
    print('Processed ' + str(total_records) + ' records, would have added ' + str(added_records) + ' to map.')


def main():
    read_from_stream(open('data/transformed.csv'))


if '__main__' == __name__:
    main()
