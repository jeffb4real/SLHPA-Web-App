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

# Derive an output .csv file from our existing .csv file
csv_input_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'SLHPA-records-phase01.csv')
csv_output_file = csv_input_file.replace('.csv', '_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
with open(csv_output_file, 'w', newline='') as outfile, open(csv_input_file, 'r', newline='') as infile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Search title, subject, and description fields for years between 1839 (the
    # invention of photography) and 1980 (approx. culmination of the photo archive).
    # When multiple valid years are found, use the highest one in the date field.
    first_record = True
    for record in reader:
        date = ''
        list_of_years = []
        # Match year(s). Notice this will match ca.1872 but won't match ca1872
        # Also, will return 1944 if given 1944-45
        pattern = r'\b(\d\d\d\d)\b'
        print (record[resource_name])
        list_of_years.extend(re.findall(pattern, record[title]))
        list_of_years.extend(re.findall(pattern, record[subject]))
        list_of_years.extend(re.findall(pattern, record[description]))
        if (list_of_years):
            print (list_of_years)
            filtered_list_of_years = []
            for year in list_of_years:
                if (int(year) > 1838 and int(year) < 1981):
                    filtered_list_of_years.append(year)
            if (filtered_list_of_years):
                date = str(max(filtered_list_of_years))
                print ("--------> %s" % date)
        print ('----')

        # Write entire record to output .csv file, populating date field (if a date was found)
        # Special exception for the first record (the header)
        if (first_record):
            date = 'date'
            first_record = False
        writer.writerow([
            record[resource_name],
            record[asset_name],
            record[file_size],
            record[title],
            record[subject],
            record[description],
            record[contributor],
            record[digital_format],
            record[url_for_file],
            date,
            record[subject_group],
            record[geo_coord_original],
            record[geo_coord_UTM],
        ])

