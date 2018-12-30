# Transform from 1980 paper map coordinates to GPS
import sys
import csv
import datetime
import pprint


def log(message):
    script_name = sys.argv[0]
    print(str(datetime.datetime.now()) + '\t'+ script_name + ': ' + message)


def map_value(value, from_start, from_end, to_start, to_end):
    if from_end == from_start:
        return value
    return (value - from_start) * (to_end - to_start) / (from_end - from_start) + to_start


# Gotten from manually observing existing data
top_coord = 18
bottom_coord = 46
top_gps = 37.73595
bottom_gps = 37.70097
left_coord = 'B7'
right_coord = 'E9'
left_gps = -122.19608
right_gps = -122.12383


def transform_vertical(value):
    return map_value(value, top_coord, bottom_coord, top_gps, bottom_gps)


asciiA = ord('A')
ascii0 = ord('0')


# Turns a string of the form [A-Z][0-9] into a number between 0 and whatever.
def to_numeric(coord):
    alpha_coord = ord(coord[0])
    numeric_coord = ord(coord[1])
    return ((alpha_coord - asciiA) * 10) + (numeric_coord - ascii0)


def transform_horizontal(value):
    return map_value(to_numeric(value), to_numeric(left_coord), to_numeric(right_coord), left_gps, right_gps)


prefix_chars = {}
vert_coords = {}
horiz_coords = {}

def increment_count(the_dict, the_value):
    if the_dict.get(the_value) is None:
        the_dict[the_value] = 0
    the_dict[the_value] += 1

# Turns a string of the form [A-Z][0-9][0-9][0-9] into GPS coordinates.
def transform_point(coords):
    if len(coords) > 4:
        prefix = coords[0:2]
        increment_count(prefix_chars, prefix)
        prefix_chars[prefix] += 1
        coords = coords[2:6]
    increment_count(vert_coords, coords[2:4])
    increment_count(horiz_coords, coords[0:2])
    tens_coord = ord(coords[2])
    ones_coord = ord(coords[3])
    vertical_coord = transform_vertical(((tens_coord - ascii0) * 10) + (ones_coord - ascii0))
    horizontal_coord = transform_horizontal(coords[0:2])
    return [horizontal_coord, vertical_coord]

horiz_errors = []
vert_errors = []

def print_details():
    log('prefix_chars:')
    pprint.pprint(prefix_chars)
    log('horiz_coords:')
    pprint.pprint(horiz_coords)
    log('vert_coords:')
    pprint.pprint(vert_coords)
    log('horiz_errors')
    print(horiz_errors)
    log('vert_errors')
    print(vert_errors)

def str_to_coords(the_string):
    if not the_string:
        return None
    if len(the_string) == 0:
        return None
    coords = the_string.replace('[', '').replace(']', '').split(',')
    if len(coords) < 2:
        return None
    horiz_coord = float(coords[0].strip())
    vert_coord = float(coords[1].strip())
    return [horiz_coord, vert_coord]

def accumulate_error(record):
    if not record.get('verified_gps_coords'):
        return
    if not record.get('geo_coord_UTM'):
        return
    verified_gps_coords = str_to_coords(record['verified_gps_coords'])
    horiz_error = abs(verified_gps_coords[0] - record['geo_coord_UTM'][0]) / abs(left_gps - right_gps)
    horiz_errors.append(horiz_error)
    vert_error = abs(verified_gps_coords[1] - record['geo_coord_UTM'][1]) / abs(top_gps - bottom_gps)
    vert_errors.append(vert_error)

def transform(infile):
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
            accumulate_error(record)
        writer.writerow(record)
    average_horiz_error = sum(horiz_errors) / len(horiz_errors)
    log(("%.2f" % average_horiz_error) + ' average_horiz_error')
    average_vert_error = sum(vert_errors) / len(vert_errors)
    log(("%.2f" % average_vert_error) + ' average_vert_error')
    log("{: >4d}".format(total_records) + ' records processed, ' + str("{: >4d}".format(transformed_records)) + ' transformed')
    # Uncomment if you want to see more details.
    # print_details()

def main():
    with open('data/merged.csv', 'r', newline='') as infile:
        transform(infile)


def check_value(message, expected_value, actual_value):
    eps = 0.000001
    if abs(expected_value - actual_value) > eps:
        log("Fail: " + message + ' Expected: ' + str(expected_value) + ', Actual: ' + str(actual_value))


def test_point(expected_horizonal, expected_vertical, old_coords):
    point = transform_point(old_coords)
    check_value('transform_point horizontal', expected_horizonal, point[0])
    check_value('transform_point vertical', expected_vertical, point[1])


def test():
    check_value('transform_vertical(top_coord)', top_gps, transform_vertical(top_coord))
    check_value('transform_vertical(bottom_coord)', bottom_gps, transform_vertical(bottom_coord))
    check_value('transform_horizontal(left_coord)', left_gps, transform_horizontal(left_coord))
    check_value('transform_horizontal(right_coord)', right_gps, transform_horizontal(right_coord))

    test_point(left_gps, top_gps, left_coord + str(top_coord))
    test_point(right_gps, bottom_gps, right_coord + str(bottom_coord))
    test_point(left_gps, 37.71362, '12B732')
    test_point(-122.19608, 37.70097, '18B746')
    test_point(-122.13737, 37.73719, '99E317')


if '__main__' == __name__:
    # test()
    main()
