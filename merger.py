import csv
import sys
import datetime
import re
import pprint
import random


# This script supercedes and replaces comber.py

# To see various statistics, set to True.
show_stats = False

def log(message):
    """ Log messages to terminal in a standard format. """
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t' + script_name + ': ' + message)


def prepend_zeros(n):
    """ Reformat the primary key column data in the 'from_dvd' file. """
    return "000" + n + '.pdf'


def number_to_pdf(n):
    """ Reformat the primary key column data in the 'transcribed' file. """
    return "{:0>8d}".format(int(n)) + '.pdf'


def read_from_stream_into_dict(file_name: str, key_function_name: callable, key_column_name: str) -> [list, dict]:
    """
    Read records from file_name into memory. Return a list of column names and a dictionary of records,
    with key ID as hash key.
    """
    the_dict = {}
    count = 0
    fieldnames = None
    with open(file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
        for record in reader:
            count += 1
            if len(record[key_column_name]) > 0:
                the_dict[key_function_name(record[key_column_name])] = record
    log(str("{: >4d}".format(len(the_dict))) +
        ' unique records read from ' + file_name + ' (total: ' + str(count) + ')')
    return fieldnames, the_dict


data_dir = 'mysite/slhpa/static/slhpa/data/'


def write(records: dict, fieldnames: list):
    """ Write a csv file of records with fieldnames fields. """
    non_numeric_keys = ''
    current_resource_number = 0
    record_count = 0
    missing_resource_names = ''
    filename = data_dir + 'merged.csv'
    outfile = open(filename, 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for _, value in sorted(records.items()):
        if value.get("resource_name"):
            writer.writerow(value)
            record_count += 1
            if len(_) > 12:
                non_numeric_keys = non_numeric_keys + ' ' + _
            num = int(_[0:8])
            if num > current_resource_number:
                current_resource_number = num
        else:
            missing_resource_names += ' ' + _
    log(str("{: >4d}".format(record_count)) +
        ' records written to ' + filename)
    log('missing resource names for: ' + missing_resource_names)
    log('non_numeric_keys: ' + non_numeric_keys)
    if show_stats:
        log('next_resource_number: ' + str(current_resource_number + 1))


def write_year_counts(scraped_records: dict):
    """ Write a .tsv file containing histogram data of photos per year. """

    # Create and fill arrays with zeros
    year_counts = [0] * 2020
    adjusted_year_counts = [0] * 2020

    # Optional randomizing of year, to account for estimates and 'circa'
    random.seed(0)
    for _, record in scraped_records.items():
        if record.get('year'):
            year_counts[int(record['year'])] += 1
            adjusted_year = int(record['year'])
            if adjusted_year % 10 == 0:
                adjusted_year = adjusted_year - 5 + round(10 * random.random())
            adjusted_year_counts[adjusted_year] += 1

    min_year = 0
    for y in range(0, 2019):
        if year_counts[y] > 0:
            min_year = y
            break
    total_count = 0
    fn = data_dir + 'year_counts.tsv'
    with open(fn, 'w', newline='') as out_file:
        out_file.write('year\tcount\n')
        for y in range(min_year, 2020):
            out_file.write(
                str(y) + '\t' + str(year_counts[y]) + '\n')
            total_count += year_counts[y]
    if show_stats:
        log(str(min_year) + ' min_year')
        log(str("{: >4d}".format(total_count)) +
            ' counts of photos with year data written to ' + fn)


def comb_addresses(scraped_fieldnames: list, scraped_records: dict):
    """
    Search for potential addresses within various fields and modify record if one is found.

    This function uses a regex list of street name types that is ordered from longest to
    shortest, so preference is given to non-abbreviations. 
    """
    scraped_fieldnames.append('address')
    addresses_found = {}

    pattern = re.compile(
        r'\d+\s\w+\s(Boulevard|Commons|Highway|Terrace|Circle|Court|Alley|Lane|Blvd|Cmns|Park|Road|Ave|Cir|Hwy|Way|Ct|Dr|Ln|Pl|Rd|St)')
    for value in scraped_records.values():
        for field in 'title', 'subject', 'description', 'description2':
            if value.get(field):
                matches = pattern.match(value[field])
                if matches:
                    value['address'] = matches.group(0)
                    addresses_found[value['resource_name']] = value['address']
                    break
    if show_stats:
        log("{: >4d}".format(len(addresses_found)) + ' addresses_found.')
        pprint.pprint(addresses_found) # for diagnosing / detailed reporting


def add_year(field_text):
    '''
    Search title, subject, and description fields for years between 1839 (the
    invention of photography) and whatever is in the code below.
    '''
    # Match year(s). Notice this will match ca.1872 but won't match ca1872.
    # Also, will return 1944 if given 1944-45.
    pattern = r'\b(\d\d\d\d)\b'

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


def comb(scraped_records, dvd_records):
    '''
    Extract year and description if possible.
    '''
    num_removed_descs = 0
    num_removed_titles = 0

    years_from_title = 0
    years_from_dvd_title = 0
    years_from_description = 0
    years_from_period_date = 0

    for key, scraped_record in scraped_records.items():
        dvd_record = dvd_records.get(key)
        scraped_record['dvd_title'] = dvd_record['Title']

        # Don't keep unuseful descriptions
        if (re.match(r'Vol\.\s+\d+\.$', scraped_record['description'])):
            scraped_record['description'] = ''
            num_removed_descs += 1
        if (re.match(r'Vol\.\s+\d+\.$', scraped_record['dvd_title'])):
            scraped_record['dvd_title'] = ''

        # Don't keep unuseful titles
        if (re.match(r'NR$', scraped_record['title'])):
            scraped_record['title'] = ''
            num_removed_titles += 1

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

    if show_stats:
        log(str("{: >4d}".format(years_from_period_date)) +
            ' years_from_period_date')
        log(str("{: >4d}".format(years_from_title)) + ' years_from_title')
        log(str("{: >4d}".format(years_from_dvd_title)) + ' years_from_dvd_title')
        log(str("{: >4d}".format(years_from_description)) +
            ' years_from_description')

        num_years_found = years_from_period_date + years_from_title + \
            years_from_dvd_title + years_from_description
        log(str("{: >4d}".format(num_years_found)) + ' num_years_found')
        log(str("{: >4d}".format(num_removed_descs)) + ' num_removed_descs')
        log(str("{: >4d}".format(num_removed_titles)) + ' num_removed_titles')


def merge_one_file(scraped_fieldnames: list, scraped_records: dict, source_filename: str, key_function: callable, key_column_name: list) -> dict:
    """
    Merge any new columns or rows from source_filename into scraped_fieldnames and scraped_records.
    """
    source_fieldnames, source_rows = read_from_stream_into_dict(
        source_filename, key_function, key_column_name)
    scraped_names_dict = {}
    source_names_dict = {}
    for s in scraped_fieldnames:
        scraped_names_dict[s] = s
    for source_fieldname in source_fieldnames:
        if source_fieldname and not scraped_names_dict.get(source_fieldname):
            scraped_fieldnames.append(source_fieldname)
            source_names_dict[source_fieldname] = source_fieldname
    for key, value in source_rows.items():
        if scraped_records.get(key) is None:
            scraped_records[key] = value
        else:
            for source_fieldname in source_names_dict:
                if value.get(source_fieldname):
                    scraped_records[key][source_fieldname] = value[source_fieldname]
    return source_rows


def main():
    """
    1. Merge historical photo metadata from multiple source csv files:
        read -> merge -> comb -> filter -> write
    2. Create histogram data (csv file) of number of photos per year

    Note: Database fields (column headings in csv file) must match the names here:
    https://github.com/jeffb4real/SLHPA-Web-App/blob/master/mysite/slhpa/models.py
    """
    scraped_fieldnames, scraped_records = read_from_stream_into_dict(
        data_dir + 'scraped.csv', str, 'resource_name')
    scraped_fieldnames.append('geo_coord_UTM')
    dvd_fieldnames, dvd_records = read_from_stream_into_dict(
        data_dir + 'V01-V64 Index.csv', prepend_zeros, 'Index Number')
    comb(scraped_records, dvd_records)
    scraped_fieldnames.append('dvd_title')
    merge_one_file(scraped_fieldnames, scraped_records,
                   data_dir + 'manually_verified.csv', str, 'resource_name')
    merge_one_file(scraped_fieldnames, scraped_records,
                   data_dir + 'transcribed.csv', number_to_pdf, 'resource_number')
    scraped_records['00000152.pdf']['description'] = 'Early farmers in San Leandro take produce to market, 1890.'
    scraped_records['00000037.pdf']['year'] = '1962'
    comb_addresses(scraped_fieldnames, scraped_records)
    write(scraped_records, scraped_fieldnames)
    write_year_counts(scraped_records)


if '__main__' == __name__:
    main()
