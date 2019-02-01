import csv
import sys
import datetime
import re
import pprint
import random


"""
This script supercedes and replaces comber.py

1. Merge historical photo metadata from multiple source csv files:
       read -> merge -> comb -> filter -> write
2. Create histogram data (csv file) of number of photos per year
"""


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
    dict = {}
    count = 0
    fieldnames = None
    with open(file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
        for record in reader:
            count += 1
            if len(record[key_column_name]) > 0:
                dict[key_function_name(record[key_column_name])] = record
    log(str("{: >4d}".format(count)) + ' total records read from ' + file_name)
    log(str("{: >4d}".format(len(dict))) +
        ' unique records read from ' + file_name)
    return fieldnames, dict


def write(records: dict, fieldnames: list):
    """ Write a csv file of records with fieldnames fields. """
    filename = 'data/merged.csv'
    outfile = open(filename, 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for _, value in sorted(records.items()):
        writer.writerow(value)
    log(str("{: >4d}".format(len(records))) +
        ' records written to ' + filename)


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

    total_count = 0
    fn = 'data/year_counts.tsv'
    with open(fn, 'w', newline='') as out_file:
        # 1839, the invention of photography, and 1980, approx. culmination of the photo archive
        for y in range(1839, 1981):
            out_file.write(
                str(y) + '\t' + str(year_counts[y]) + '\t' + str(adjusted_year_counts[y]) + '\n')
            total_count += year_counts[y]
    log(str("{: >4d}".format(total_count)) + ' year counts written to ' + fn)


def comb_addresses(scraped_fieldnames: list, scraped_records: dict):
    """ Search for potential addresses within various fields and modify record if one is found. """
    scraped_fieldnames.append('address')
    addresses_found = {}
    pattern = re.compile(
        r'\d+\s\w+\s(Ave|St|Boulevard|Blvd|Dr|Lane|Ln|Court|Ct|Road|Rd|Way|Pl|Highway|Hwy|Terrace|Alley|Circle|Cir|Park|Commons|Cmns)')
    for value in scraped_records.values():
        for field in 'title', 'subject', 'description', 'description2':
            if value.get(field):
                matches = pattern.match(value[field])
                if matches:
                    value['address'] = matches.group(0)
                    addresses_found[value['resource_name']] = value['address']
                    break
    log("{: >4d}".format(len(addresses_found)) + ' addresses_found.')
    # pprint.pprint(addresses_found) # for diagnosing / detailed reporting


def comb_years(scraped_fieldnames: list, scraped_records: dict, from_dvd: dict):
    """
    Search title, subject, and description fields for years between 1839 (the
    invention of photography) and 1980 (approx. culmination of the photo archive).
    When multiple valid years are found, use the highest one in the date field.
    """
    scraped_fieldnames.append('description2')
    num_years_found = 0
    num_descs_found = 0
    for key, value in scraped_records.items():
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
                value['description2'] = title_from_dvd
                num_descs_found += 1
    log("{: >4d}".format(num_years_found) + ' years added.')
    log("{: >4d}".format(num_descs_found) + ' descriptions added.')


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
    scraped_fieldnames, scraped_records = read_from_stream_into_dict(
        'data/scraped.csv', str, 'resource_name')
    scraped_fieldnames.append('geo_coord_UTM')
    merge_one_file(scraped_fieldnames, scraped_records,
                   'data/manually_verified.csv', str, 'resource_name')
    merge_one_file(scraped_fieldnames, scraped_records,
                   'data/transcribed.csv', number_to_pdf, 'resource_number')
    dvd_records = merge_one_file(scraped_fieldnames, scraped_records,
                                 'data/V01-V64 Index.csv', prepend_zeros, 'Index Number')
    comb_years(scraped_fieldnames, scraped_records, dvd_records)
    comb_addresses(scraped_fieldnames, scraped_records)
    write(scraped_records, scraped_fieldnames)
    write_year_counts(scraped_records)


if '__main__' == __name__:
    main()
