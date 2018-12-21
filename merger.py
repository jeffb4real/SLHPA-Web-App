# Merge historical photo metadata from multiple source csv files
import csv

def prepend_zeros(n):
    return "000" + n + '.pdf'

def number_to_pdf(n):
    return "{:0>8d}".format(int(n)) + '.pdf'

def read_from_stream_into_dict(infile, key_function, key_column):
    dict = {}
    reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for record in reader:
        if len(record[key_column]) > 0:
            dict[key_function(record[key_column])] = record
    return dict

def write(scraped, fieldnames):
    outfile = open('data/merged.csv', 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for value in scraped.values():
        writer.writerow(value)
    print('Wrote ' + str(len(scraped)) + ' total_records.')

def merge(scraped, transcribed, manually_entered, from_dvd):
    for key, value in scraped.items():
        if transcribed.get(key) is not None:
            value['geo_coord_original'] = transcribed[key]['geo_coord_original']
            value['year'] = transcribed[key]['year']
    for key, value in manually_entered.items():
        scraped[key] = value

def main():
    with open('data/scraped.csv', 'r', newline='') as infile:
        scraped = read_from_stream_into_dict(infile, str, 'resource_name')
    with open('data/transcribed.csv', 'r', newline='') as infile:
        transcribed = read_from_stream_into_dict(infile, number_to_pdf, 'resource_number')
    with open('data/manually-entered.csv', 'r', newline='') as infile:
        manually_entered = read_from_stream_into_dict(infile, str, 'resource_name')
    with open('data/V01-V64 Index.csv', 'r', newline='') as infile:
        from_dvd = read_from_stream_into_dict(infile, prepend_zeros, 'Index Number')

    merge(scraped, transcribed, manually_entered, from_dvd)
    fieldnames = None
    with open('data/scraped.csv', 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
    fieldnames.append('geo_coord_original')
    fieldnames.append('geo_coord_UTM')
    fieldnames.append('date')
    fieldnames.append('year')
    fieldnames.append('subject_group')
    write(scraped, fieldnames)

if '__main__' == __name__:
    main()
