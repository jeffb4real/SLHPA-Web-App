# Read from csv file (or stdin) and write to Google Maps
import sys
import csv

def placePin(horizontal, vertical, name, description, photo):
    print('TODO : place pin for : ' + name) 

def handleRecord(record):
    geoCoords = record['geo_coord_UTM']
    if geoCoords is not None and len(geoCoords) > 0:
        coords = geoCoords.split(',')
        if len(coords) == 2:
            horizontal = float(coords[0])
            vertical = float(coords[1])
            placePin(horizontal, vertical,
                     record['asset_name'], record['description'], record['url_for_file'])

def readFromStream(inputStream):
    reader = csv.DictReader(inputStream, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for record in reader:
        handleRecord(record)

def clearExistingPins():
    print('TODO : implement clearExistingPins')

def main():
    if (len(sys.argv) > 1):
        clearExistingPins()
        readFromStream(open(sys.argv[1]))
    else:
        print('Must pass input file name as first command line parameter.')

def test():
    testData = [ {'resource_name' : '00000001.pdf',
                  'asset_name' : 'Alameda County Courthouse in San Leandro, ca 1856',
                  'file_size' : '371.97 KB',
                  'title' : 'Alameda County Courthouse in San Leandro, ca 1856',
                  'subject' : 'Alameda County Courthouse',
                  'description' : '',
                  'contributor' : 'Shaffer, Harry',
                  'digital_format' : 'PDF',
                  'url_for_file' : 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5138/0',
                  'date' : '',
                  'subject_group' : '',
                  'geo_coord_original' : '14 D6 25',
                  'geo_coord_UTM' : '37.727205, -122.1531815625'
                  },
                  {'resource_name' : '00000002.pdf',
                  'asset_name' : 'Bank of San Leandro, ca 1893',
                  'file_size' : '365.50 KB',
                  'title' : 'Bank of San Leandro, ca 1893',
                  'subject' : '',
                  'description' : '',
                  'contributor' : 'Galvan, Andy',
                  'digital_format' : 'PDF',
                  'url_for_file' : 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5139/0',
                  'date' : '',
                  'subject_group' : '',
                  'geo_coord_original' : '',
                  'geo_coord_UTM' : ''
                  },
                  {'resource_name' : '00000002.pdf',
                  'asset_name' : 'Bank of San Leandro, ca 1893',
                  'file_size' : '365.50 KB',
                  'title' : 'Bank of San Leandro, ca 1893',
                  'subject' : '',
                  'description' : '',
                  'contributor' : 'Galvan, Andy',
                  'digital_format' : 'PDF',
                  'url_for_file' : 'https://sanle.ent.sirsi.net/client/en_US/search/asset/5139/0',
                  'date' : '',
                  'subject_group' : '',
                  'geo_coord_original' : '',
                  'geo_coord_UTM' : None
                  }
                 ]
    for record in testData:
        handleRecord(record)

test()

