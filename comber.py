import csv
import os
import sys
import re
import time

# All fields for a single record
resource_name = 0
asset_name = 1
file_size = 2
title = 3
subject = 4
description = 5
contributor = 6
digital_format = 7
url_for_file = 8
date = 9
subject_group = 10
geo_coord_original = 11
geo_coord_UTM = 12

# First, create an array of entries in the Title field, from document on photo archive DVD
csv_input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'V01-V64 Index.csv')
title_fields = []
with open(csv_input_file, 'r', newline='') as infile:
    reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for record in reader:
        # 2nd array element is the Title field; this is the only useful descriptive field in this document
        title_fields.append(record[2])

# Derive an output .csv file from our existing .csv file
csv_input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'SLHPA-records-phase01.csv')
csv_output_file = csv_input_file.replace('.csv', '_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
with open(csv_output_file, 'w', newline='') as outfile, open(csv_input_file, 'r', newline='') as infile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Search title, subject, and description fields for years between 1839 (the
    # invention of photography) and 1980 (approx. culmination of the photo archive).
    # When multiple valid years are found, use the highest one in the date field.
    num_years_found = 0
    num_descs_found = 0
    desc_index = 0
    num_records = 0
    num_removed_descs = 0
    first_record = True
    for record in reader:
        date = ''
        description2 = ''
        list_of_years = []
        # 1.
        # Match year(s). Notice this will match ca.1872 but won't match ca1872
        # Also, will return 1944 if given 1944-45
        pattern = r'\b(\d\d\d\d)\b'
        print (record[resource_name])
        list_of_years.extend(re.findall(pattern, record[title]))
        list_of_years.extend(re.findall(pattern, record[subject]))
        list_of_years.extend(re.findall(pattern, record[description]))
        list_of_years.extend(re.findall(pattern, title_fields[desc_index]))
        if (list_of_years):
            print (list_of_years)
            filtered_list_of_years = []
            for year in list_of_years:
                if (int(year) > 1838 and int(year) < 1981):
                    filtered_list_of_years.append(year)
            if (filtered_list_of_years):
                date = str(max(filtered_list_of_years))
                print ("--------> %s" % date)
                num_years_found+=1

        # 2.
        # Compare description fields; add description2 if they don't match
        if ((title_fields[desc_index] not in record[description]) and
            (title_fields[desc_index] not in record[title]) and
            (title_fields[desc_index] != 'NR') ):
            description2 = title_fields[desc_index]
            num_descs_found+=1
        print ('----')

        # 3.
        # Don't need to keep unuseful descriptions
        description1 = record[description]
        if (re.match(r'Vol\.\s+\d+$', description1)):
            description1 = ''
            num_removed_descs+=1

        # Write entire record to output .csv file, populating date field (if a date was found)
        # Special exception for the first record (the header)
        if (first_record):
            date = 'date'
            description1 = 'description'
            description2 = 'description_from_DVD'
            first_record = False
        writer.writerow([
            record[resource_name],
            record[asset_name],
            record[file_size],
            record[title],
            record[subject],
            description1,
            description2,
            record[contributor],
            record[digital_format],
            record[url_for_file],
            date,
            record[subject_group],
            record[geo_coord_original],
            record[geo_coord_UTM],
        ])

        desc_index+=1
        num_records+=1

print ("**Found %d title fields" % len(title_fields))
print ("**Processed %d records" % num_records)
print ("\n**Found and added %d years to new .csv file" % num_years_found)
print ("**Added %d descriptions to new .csv file" % num_descs_found)
print ("**Removed %d unuseful descriptions\n" % num_removed_descs)

