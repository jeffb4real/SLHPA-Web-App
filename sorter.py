import sys
import csv
import datetime
import pprint
import random

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)

def read_from_stream_into_dict(file_name):
    dict = {}
    fieldnames = None
    with open(file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
        for record in reader:
            if not record.get('geo_coord_original'):
                continue
            key = record['geo_coord_original']
            if (len(key) < 6):
                continue
            record['geo_coord_original'] = key[2:6] + key[0:2]
            dict[record['resource_name']] = record
    log(str("{: >4d}".format(len(dict))) + ' records read from ' + file_name)
    return fieldnames, dict 

def get_record_key(record):
    return record['resource_name'] + ' ' + record['geo_coord_original']

def main():
    fieldnames, records = read_from_stream_into_dict('data/transformed.csv')
#    sorted_by_value = sorted(records.items(), key=get_record_key)
    with open('data/sorted.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
#        for record in sorted_by_value:
#            writer.writerow(record)

if '__main__' == __name__:
    main()
