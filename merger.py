# Merge historical photo metadata from multiple source csv files
import csv
import sys
import datetime
import re

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)

# Reformat the primary key column data in the 'from_dvd' file.
def prepend_zeros(n):
    return "000" + n + '.pdf'

# Reformat the primary key column data in the 'transcribed' file.
def number_to_pdf(n):
    return "{:0>8d}".format(int(n)) + '.pdf'

def read_from_stream_into_dict(file_name, key_function, key_column):
    dict = {}
    with open(file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for record in reader:
            if len(record[key_column]) > 0:
                dict[key_function(record[key_column])] = record
    log(str("{: >4d}".format(len(dict))) + ' records read from ' + file_name)
    return dict

def write(scraped, fieldnames):
    fn = 'data/merged.csv'
    outfile = open(fn, 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for key, value in sorted(scraped.items()):
       writer.writerow(value)
    log(str("{: >4d}".format(len(scraped))) + ' records written to ' + fn)

def comb(scraped, from_dvd):
    # Search title, subject, and description fields for years between 1839 (the
    # invention of photography) and 1980 (approx. culmination of the photo archive).
    # When multiple valid years are found, use the highest one in the date field.
    num_years_found = 0
    num_descs_found = 0
    for key, value in scraped.items():
        record_from_dvd = from_dvd.get(key)
        if record_from_dvd is not None:
            if value.get('year') is None or len(value['year']) == 0:
                # Match year(s). Notice this will match ca.1872 but won't match ca1872
                # Also, will return 1944 if given 1944-45
                list_of_years = []
                pattern = r'\b(\d\d\d\d)\b'
                list_of_years.extend(re.findall(pattern, value['title']))
                list_of_years.extend(re.findall(pattern, value['subject']))
                list_of_years.extend(re.findall(pattern, value['description']))
                if (list_of_years):
                    filtered_list_of_years = []
                    for year in list_of_years:
                        if (int(year) > 1838 and int(year) < 1981):
                            filtered_list_of_years.append(year)
                    if (filtered_list_of_years):
                        value['year'] = str(max(filtered_list_of_years))
                        num_years_found += 1

            # Compare description fields; add description from DVD if they don't match
            title_from_dvd = record_from_dvd['Title']
            if ((title_from_dvd not in value['description']) and
                (title_from_dvd not in value['title']) and
                (title_from_dvd != 'NR')):
                value['description'] += title_from_dvd
                num_descs_found += 1
    log(str(num_years_found) + ' years added.')
    log(str(num_descs_found) + ' descriptions added.')

# Merge data into scraped from all other sources.
def merge(scraped, transcribed, manually_entered, from_dvd):
    for key, value in scraped.items():
        if transcribed.get(key) is not None:
            value['geo_coord_original'] = transcribed[key]['geo_coord_original']
            value['year'] = transcribed[key]['year']
    for key, value in manually_entered.items():
        scraped[key] = value
    comb(scraped, from_dvd)

def main():
    scraped = read_from_stream_into_dict('data/scraped.csv', str, 'resource_name')
    transcribed = read_from_stream_into_dict('data/transcribed.csv', number_to_pdf, 'resource_number')
    manually_entered = read_from_stream_into_dict('data/manually-entered.csv', str, 'resource_name')
    from_dvd = read_from_stream_into_dict('data/V01-V64 Index.csv', prepend_zeros, 'Index Number')

    for value in scraped.values():
        value['geo_coord_original'] = None
        value['geo_coord_UTM'] = None
        value['date'] = None
        value['year'] = None
        value['subject_group'] = None

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
