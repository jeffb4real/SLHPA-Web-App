import sys
import csv
import datetime

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
                if not record.get('geo_coord_original'):
                    continue
                key = record['geo_coord_original']
                if (len(key) < 6):
                    continue
                record['geo_coord_original'] = key[2:6] + key[0:2]
                dict[record['resource_name']] = record
        log(str("{: >4d}".format(len(dict))) + ' records read from ' + file_name)
        return fieldnames, dict 

    def get_record_key(self, array_record):
        return array_record[self.field_indices['geo_coord_original']] + ' ' + array_record[self.field_indices['resource_name']]

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

    def main(self):
        fieldnames, dict_records = self.read_from_stream_into_dict('data/transformed.csv')
        i = 0
        for f in fieldnames:
            self.field_indices[f] = i
            self.field_names_dict[i] = f
            i += 1
        array_records = []
        for r in dict_records.values():
            array_records.append(self.to_array(r))
        sorted_by_value = sorted(array_records, key=self.get_record_key)
        with open('data/sorted.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for record in sorted_by_value:
                writer.writerow(self.to_dict(record))
        log(str("{: >4d}".format(len(sorted_by_value))) + ' records written to sorted.csv')

if '__main__' == __name__:
    Sorter().main()
