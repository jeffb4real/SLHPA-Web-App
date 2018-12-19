# Transform from 1980 paper map coordinates to GPS
import sys
import csv


def map_value(value, from_start, from_end, to_start, to_end):
    if from_end == from_start:
        return value
    return (value - from_start) * (to_end - to_start) / (from_end - from_start) + to_start


# Gotten from manually observing existing data
top_coord = 18
bottom_coord = 46
top_gps = 37.73595
bottom_gps = 37.70097


def transform_vertical(value):
    return map_value(value, top_coord, bottom_coord, top_gps, bottom_gps)


left_coord = 'B7'
right_coord = 'E9'
left_gps = -122.19608
right_gps = -122.12383

asciiA = ord('A')
ascii0 = ord('0')


# Turns a string of the form [A-Z][0-9] into a number between 0 and whatever.
def to_numeric(coord):
    alpha_coord = ord(coord[0])
    numeric_coord = ord(coord[1])
    return ((alpha_coord - asciiA) * 10) + (numeric_coord - ascii0)


def transform_horizontal(value):
    return map_value(to_numeric(value), to_numeric(left_coord), to_numeric(right_coord), left_gps, right_gps)


# Turns a string of the form [A-Z][0-9][0-9][0-9] into GPS coordinates.
def transform_point(coords):
    if len(coords) > 4:
        coords = coords[2:6]
    tens_coord = ord(coords[2])
    ones_coord = ord(coords[3])
    vertical_coord = transform_vertical(((tens_coord - ascii0) * 10) + (ones_coord - ascii0))
    horizontal_coord = transform_horizontal(coords[0:2])
    return [horizontal_coord, vertical_coord]


def read_from_stream(infile):
    reader = csv.DictReader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outfile = open('data/transformed.csv', 'w', newline='')
    writer = csv.DictWriter(outfile, reader.fieldnames, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    total_records = 0
    transformed_records = 0
    for record in reader:
        total_records += 1
        record['geo_coord_original'] = record['geo_coord_original'].replace(' ', '')
        if len(record['geo_coord_original']) >= 4:
            record['geo_coord_UTM'] = transform_point(record['geo_coord_original'])
            transformed_records += 1
        writer.writerow(record)
    print('Processed ' + str(total_records) + ' records, transformed ' + str(transformed_records))


def main():
    with open('data/combed.csv', 'r', newline='') as infile:
        read_from_stream(infile)


def check_value(message, expected_value, actual_value):
    eps = 0.00001
    if abs(expected_value - actual_value) > eps:
        print("Fail: " + str(message) + ' Expected: ' + str(expected_value) + ', Actual: ' + str(actual_value))
    else:
        print("Pass: " + message)


def test():
    check_value('transform_vertical(top_coord)', top_gps, transform_vertical(top_coord))
    check_value('transform_vertical(bottom_coord)', bottom_gps, transform_vertical(bottom_coord))
    check_value('transform_horizontal(left_coord)', left_gps, transform_horizontal(left_coord))
    check_value('transform_horizontal(right_coord)', right_gps, transform_horizontal(right_coord))

    upper_left = transform_point(left_coord + str(top_coord))
    check_value('transform_point left', left_gps, upper_left[0])
    check_value('transform_point top', top_gps, upper_left[1])
    lower_right = transform_point(right_coord + str(bottom_coord))
    check_value('transform_point right', right_gps, lower_right[0])
    check_value('transform_point bottom', bottom_gps, lower_right[1])

    print('')
    print('transform lower right: ' + str(transform_point('99' + right_coord + '46')))
    print('transform test data 1: ' + str(transform_point('D625')))


if '__main__' == __name__:
    print('----- test -----')
    test()
    print('----- main -----')
    main()
