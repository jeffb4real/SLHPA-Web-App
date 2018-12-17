# Read from csv file (or stdin) and write to Google Maps
import sys
import csv


def place_pin(horizontal, vertical, name, description, photo):
    print('TODO : place pin for : ' + name)


def handle_record(record):
    geo_coords = record['geo_coord_UTM']
    if geo_coords is not None and len(geo_coords) > 0:
        coords = geo_coords.replace('[', '').replace(']', '').split(',')
        if len(coords) == 2:
            horizontal = float(coords[0])
            vertical = float(coords[1])
            place_pin(horizontal, vertical,
                      record['asset_name'], record['description'], record['url_for_file'])
        return 1
    else:
        return 0


def read_from_stream(input_stream):
    reader = csv.DictReader(input_stream, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    total_records = 0
    added_records = 0
    for record in reader:
        added_records += handle_record(record)
        total_records += 1
    print('Processed ' + str(total_records) + ' records, would have added ' + str(added_records) + ' to map.')


def main():
    if (len(sys.argv) > 1):
        read_from_stream(open(sys.argv[1]))
    else:
        print('Must pass input file name as first command line parameter.')


def test():
    test_data = [{'resource_name': '00000001.pdf',
                  'asset_name': 'Alameda County Courthouse in San Leandro, ca 1856',
                  'file_size': '371.97 KB',
                  'title': 'Alameda County Courthouse in San Leandro, ca 1856',
                  'subject': 'Alameda County Courthouse',
                  'description': '',
                  'contributor': 'Shaffer, Harry',
                  'digital_format': 'PDF',
                  'url_for_file': 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5138/0',
                  'date': '',
                  'subject_group': '',
                  'geo_coord_original': '14 D6 25',
                  'geo_coord_UTM': '37.727205, -122.1531815625'
                  },
                 {'resource_name': '00000002.pdf',
                  'asset_name': 'Bank of San Leandro, ca 1893',
                  'file_size': '365.50 KB',
                  'title': 'Bank of San Leandro, ca 1893',
                  'subject': '',
                  'description': '',
                  'contributor': 'Galvan, Andy',
                  'digital_format': 'PDF',
                  'url_for_file': 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5139/0',
                  'date': '',
                  'subject_group': '',
                  'geo_coord_original': '',
                  'geo_coord_UTM': ''
                  },
                 {'resource_name': '00000002.pdf',
                  'asset_name': 'Bank of San Leandro, ca 1893',
                  'file_size': '365.50 KB',
                  'title': 'Bank of San Leandro, ca 1893',
                  'subject': '',
                  'description': '',
                  'contributor': 'Galvan, Andy',
                  'digital_format': 'PDF',
                  'url_for_file': 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5139/0',
                  'date': '',
                  'subject_group': '',
                  'geo_coord_original': '',
                  'geo_coord_UTM': None
                  }
                 ]
    for record in test_data:
        handle_record(record)
    read_from_stream(open('data/transformed.csv'))


if '__main__' == __name__:
    # main()
    test()
