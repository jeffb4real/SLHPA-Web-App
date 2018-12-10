# Read from csv file (or stdin) and write to Google Maps
import sys
import csv

def handleRecord(record):
    if len(record['geo_coord_UTM']) > 0:
        print(record)

def readFromStream(inputStream):
    reader = csv.DictReader(inputStream, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for record in reader:
        handleRecord(record)

def clearExistingPins():
    print('TODO : implement clearExistingPins')

def main():
    clearExistingPins()
    if (len(sys.argv) > 1):
        readFromStream(open(sys.argv[1]))
    else:
        readFromStream(sys.stdin)

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
                  }
                 ]
    for record in testData:
        handleRecord(record)

test()

