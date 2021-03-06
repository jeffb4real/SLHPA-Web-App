import csv
import os
import sys
import re
import time
import datetime


def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)


def add_year(field_text):
    '''
    Search title, subject, and description fields for years between 1839 (the
    invention of photography) and 1980 (approx. culmination of the photo archive).
    '''
    # Match year(s). Notice this will match ca.1872 but won't match ca1872.
    # Also, will return 1944 if given 1944-45.
    pattern = r'\b(\d\d\d\d)\b'
    pattern2 = r'ca(\d\d\d\d)\b'

    list_of_years = re.findall(pattern, field_text)
    if (list_of_years):
        filtered_list_of_years = []
        for year in list_of_years:
            if (int(year) > 1838 and int(year) < 2019):
                filtered_list_of_years.append(year)
        if (filtered_list_of_years):
            return str(max(filtered_list_of_years))
    return None


def add_year_if_possible(scraped_record, field_name):
    date = add_year(scraped_record[field_name])
    if date:
        scraped_record['year'] = date
        return True
    return False


def comb(scraped_fieldnames, scraped_records, dvd_fieldnames, dvd_records):
    '''
    Extract year and description if possible.
    '''
    num_descs_found = 0
    num_removed_descs = 0

    years_from_title = 0
    years_from_dvd_title = 0
    years_from_description = 0
    years_from_period_date = 0

    for key, scraped_record in scraped_records.items():
        dvd_record = dvd_records.get(key)
        scraped_record['dvd_title'] = dvd_record['Title']

        # Don't keep unuseful descriptions
        if (re.match(r'Vol\.\s+\d+$', scraped_record['description'])):
            scraped_record['description'] = ''
            num_removed_descs += 1
        if (re.match(r'Vol\.\s+\d+$', scraped_record['dvd_title'])):
            scraped_record['dvd_title'] = ''
            num_removed_descs += 1

        if add_year_if_possible(scraped_record, 'period_date'):
            years_from_period_date += 1
        else:
            if add_year_if_possible(scraped_record, 'title'):
                years_from_title += 1
            else:
                if add_year_if_possible(scraped_record, 'dvd_title'):
                    years_from_dvd_title += 1
                else:
                    if add_year_if_possible(scraped_record, 'description'):
                        years_from_description += 1

    log(str("{: >4d}".format(years_from_period_date)) + ' years_from_period_date')
    log(str("{: >4d}".format(years_from_title)) + ' years_from_title')
    log(str("{: >4d}".format(years_from_dvd_title)) + ' years_from_dvd_title')
    log(str("{: >4d}".format(years_from_description)) + ' years_from_description')

    num_years_found = years_from_title + years_from_dvd_title + years_from_description
    log(str("{: >4d}".format(num_years_found)) + ' num_years_found')
    log(str("{: >4d}".format(num_descs_found)) + ' num_descs_found')
    log(str("{: >4d}".format(num_removed_descs)) + ' num_removed_descs')


def prepend_zeros(n):
    """ Reformat the primary key column data in the 'from_dvd' file. """
    return "000" + n + '.pdf'


data_path = 'mysite/slhpa/static/slhpa/data/'


def read_from_stream_into_dict(file_name: str, key_function_name: callable,
                                key_column_name: str) -> [list, dict]:
    """
    Read records from file_name into memory.
    Return a list of column names and a dictionary of records,
    with key ID as hash key.
    """
    the_dict = {}
    count = 0
    fieldnames = None
    with open(data_path + file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
        for record in reader:
            count += 1
            if len(record[key_column_name]) > 0:
                the_dict[key_function_name(record[key_column_name])] = record
    log(str("{: >4d}".format(count)) + ' total records read from ' + file_name)
    log(str("{: >4d}".format(len(the_dict))) + ' unique records read from ' + file_name)
    return fieldnames, the_dict


def write(records: dict, fieldnames: list, filename: str):
    filename = data_path + filename
    outfile = open(filename, 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for _, value in sorted(records.items()):
        writer.writerow(value)
    log(str("{: >4d}".format(len(records))) + ' records written to ' + filename)


def main():
    scraped_fieldnames, scraped_records = read_from_stream_into_dict(
        'scraped.csv', str, 'resource_name')
    dvd_fieldnames, dvd_records = read_from_stream_into_dict(
        'V01-V64 Index.csv', prepend_zeros, 'Index Number')
    comb(scraped_fieldnames, scraped_records, dvd_fieldnames, dvd_records)
    write(scraped_records,
          ['resource_name', 'year', 'title', 'description', 'dvd_title', 'subject',
           'contributor', 'url_for_file', 'asset_name', 'period_date', 'file_size',
           'digital_format'],
          'combed.csv')


if '__main__' == __name__:
    log('Functionality now included in other python scripts.')
    # main()
