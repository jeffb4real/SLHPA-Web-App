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
    return [vertical_coord, horizontal_coord]


def read_from_stream(the_file_name):
    with open(the_file_name, 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        i = 0;
        for record in reader:
            i += 1
        print('Would have processed ' + str(i) + ' records')


def main():
    if (len(sys.argv) > 1):
        read_from_stream(sys.argv[1])
    else:
        print('Read from stdin not implemented yet')


def test():
    print('transform top: ' + str(transform_vertical(top_coord)))
    print('transform bottom: ' + str(transform_vertical(bottom_coord)))
    print('transform left: ' + str(transform_horizontal(left_coord)))
    print('transform right: ' + str(transform_horizontal(right_coord)))
    print('transform upper left: ' + str(transform_point(left_coord + '18')))
    print('transform lower right: ' + str(transform_point(right_coord + '46')))
    print('transform lower right: ' + str(transform_point('99' + right_coord + '46')))
    print('transform test data 1: ' + str(transform_point('D625')))


if '__main__' == __name__:
    main()
    # test()
