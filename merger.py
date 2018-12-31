import csv
import sys
import datetime
import re
import pprint

# Merge historical photo metadata from multiple source csv files
# This script supercedes and replaces comber.py

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)


# Reformat the primary key column data in the 'from_dvd' file.
def prepend_zeros(n):
    return "000" + n + '.pdf'


# Reformat the primary key column data in the 'transcribed' file.
def number_to_pdf(n):
    return "{:0>8d}".format(int(n)) + '.pdf'


def read_from_stream_into_dict(file_name, key_function_name, key_column):
    dict = {}
    fieldnames = None
    with open(file_name, 'r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames
        for record in reader:
            if len(record[key_column]) > 0:
                dict[key_function_name(record[key_column])] = record
    log(str("{: >4d}".format(len(dict))) + ' records read from ' + file_name)
    return fieldnames, dict


def write(scraped, fieldnames):
    fn = 'data/merged.csv'
    outfile = open(fn, 'w', newline='')
    writer = csv.DictWriter(outfile, fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for key, value in sorted(scraped.items()):
       writer.writerow(value)
    log(str("{: >4d}".format(len(scraped))) + ' records written to ' + fn)


def comb_addresses(scraped_fieldnames, scraped):
    scraped_fieldnames.append('address')
    addresses_found = {}
    pattern = re.compile(r'\d+\s\w+\s(Ave|St|Blvd|Boulevard)')
    for value in scraped.values():
        for field in 'title', 'subject', 'description', 'description2':
            if value.get(field):
                matches = pattern.match(value[field])
                if matches:
                    value['address'] = matches.group(0)
                    addresses_found[value['resource_name']] = value['address']
                    break
    log("{: >4d}".format(len(addresses_found)) + ' addresses_found.')
    # pprint.pprint(addresses_found) # for diagnosing / detailed reporting


def comb_years(scraped_fieldnames, scraped, from_dvd):
    scraped_fieldnames.append('description2')

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

            # TODO : create second description column
            # Compare description fields; add description from DVD if they don't match
            title_from_dvd = record_from_dvd['Title']
            if ((title_from_dvd not in value['description']) and
                (title_from_dvd not in value['title']) and
                (title_from_dvd != 'NR')):
                value['description2'] = title_from_dvd
                num_descs_found += 1
    log("{: >4d}".format(num_years_found) + ' years added.')
    log("{: >4d}".format(num_descs_found) + ' descriptions added.')


# Merge any new columns or rows from source filename into scraped_fieldnames and scraped rows.
def merge_one_file(scraped_fieldnames, scraped, filename, key_function, key_column):
    source_fieldnames, source_rows = read_from_stream_into_dict(filename, key_function, key_column)
    scraped_names_dict = {}
    source_names_dict = {}
    for s in scraped_fieldnames:
        scraped_names_dict[s] = s
    for source_fieldname in source_fieldnames:
        if source_fieldname and not scraped_names_dict.get(source_fieldname):
            scraped_fieldnames.append(source_fieldname)
            source_names_dict[source_fieldname] = source_fieldname
    for key, value in source_rows.items():
        if scraped.get(key) is None:
            scraped[key] = value
        else:
            for source_fieldname in source_names_dict:
                if value.get(source_fieldname):
                    scraped[key][source_fieldname] = value[source_fieldname]
    return source_rows


def main():
    scraped_fieldnames, scraped = read_from_stream_into_dict('data/scraped.csv', str, 'resource_name')
    scraped_fieldnames.append('geo_coord_UTM')
    merge_one_file(scraped_fieldnames, scraped, 'data/manually-entered.csv', str, 'resource_name')
    merge_one_file(scraped_fieldnames, scraped, 'data/transcribed.csv', number_to_pdf, 'resource_number')
    from_dvd = merge_one_file(scraped_fieldnames, scraped, 'data/V01-V64 Index.csv', prepend_zeros, 'Index Number')
    comb_years(scraped_fieldnames, scraped, from_dvd)
    comb_addresses(scraped_fieldnames, scraped)
    write(scraped, scraped_fieldnames)


if '__main__' == __name__:
    main()
