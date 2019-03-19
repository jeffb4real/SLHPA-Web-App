import csv
import os
import sys
import re
import time
import datetime

def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)

# All fields for a single record
resource_name = 0
asset_name = 1
file_size = 2
title = 3
subject = 4
description = 5
contributor = 6
period_date = 7
digital_format = 8
url_for_file = 9
date = 10
desc2 = 11

data_path = 'mysite/slhpa/static/slhpa/data'

# Match year(s). Notice this will match ca.1872 but won't match ca1872.
# Also, will return 1944 if given 1944-45.
pattern = r'\b(\d\d\d\d)\b'

# Search title, subject, and description fields for years between 1839 (the
# invention of photography) and 1980 (approx. culmination of the photo archive).
# When multiple valid years are found, use the highest one in the date field.
def add_year(field_text):
    list_of_years = re.findall(pattern, field_text)
    if (list_of_years):
        filtered_list_of_years = []
        for year in list_of_years:
            if (int(year) > 1838 and int(year) < 2019):
                filtered_list_of_years.append(year)
        if (filtered_list_of_years):
            return str(max(filtered_list_of_years))
    return None

# Create an array of Title field records, from document on photo archive DVD
csv_input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), data_path, 'V01-V64 Index.csv')
title_fields = []
with open(csv_input_file, 'r', newline='') as infile:
    reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for record in reader:
        # 2nd array element is the Title field; this is the only useful descriptive field in this document
        title_fields.append(record[2])

# Derive an output .csv file from our existing .csv file
csv_input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), data_path, 'scraped.csv')
csv_output_file = csv_input_file.replace('scraped.csv', 'combed.csv')
with open(csv_output_file, 'w', newline='') as outfile, open(csv_input_file, 'r', newline='') as infile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    num_years_found = 0
    num_descs_found = 0
    num_records = 0
    num_removed_descs = 0
    first_record = True
    desc_index = 0
    for record in reader:
        record.extend([''])
        record.extend([''])
        # Compare description fields; add description2 if they don't match
        record[desc2] = ''
        if ((title_fields[desc_index] not in record[description]) and
            (title_fields[desc_index] not in record[title]) and
            (title_fields[desc_index] != 'NR') ):
            record[desc2] = title_fields[desc_index]
            num_descs_found+=1

        # Don't keep unuseful descriptions
        if (re.match(r'Vol\.\s+\d+$', record[description])):
            record[description] = ''
            num_removed_descs+=1
        if (re.match(r'Vol\.\s+\d+$', record[desc2])):
            record[desc2] = ''
            num_removed_descs+=1

        # TODO : look at period_date first, may have to expand pattern to match MM/DD/YYYY?
        date = add_year(record[title])
        if not date:
            date = add_year(record[description])
        if not date:
            date = add_year(record[desc2])
        if not date:
            date = add_year(record[subject])
        if date:
            num_years_found += 1

        # Write entire record to output .csv file, populating date field (if a date was found)
        # Special exception for the first record (the header)
        if (first_record):
            date = 'date'
            record[description] = 'description'
            record[desc2] = 'description_from_DVD'
            first_record = False
        writer.writerow([
            record[resource_name],
            record[asset_name],
            record[file_size],
            record[title],
            record[subject],
            record[description],
            record[desc2],
            record[contributor],
            record[digital_format],
            record[url_for_file],
            date,
        ])

        desc_index+=1
        num_records+=1

log("Found %d title fields" % len(title_fields))
log("Processed %d records" % num_records)
log("Found and added %d years to new .csv file" % num_years_found)
log("Added %d descriptions to new .csv file" % num_descs_found)
log("Removed %d unuseful descriptions" % num_removed_descs)
