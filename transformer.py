# Transform from 1980 paper map coordinates to GPS


def mapvalue(value, from_start, from_end, to_start, to_end):
    if from_end == from_start:
        return value
    return (value - from_start) * (to_end - to_start) / (from_end - from_start) + to_start


# Gotten from manually observing existing data
top_coord = 18
bottom_coord = 46
top_gps = 37.73595
bottom_gps = 37.70097


def transform_vertical(value):
    return mapvalue(value, top_coord, bottom_coord, top_gps, bottom_gps)


leftCoord = 'B7'
rightCoord = 'E9'
leftGPS = -122.19608
rightGPS = -122.12383

asciiA = ord('A')
ascii0 = ord('0')


# Turns a string of the form [A-Z][0-9] into a number between 0 and whatever.
def to_numeric(coord):
    alpha_coord = ord(coord[0])
    numeric_coord = ord(coord[1])
    return ((alpha_coord - asciiA) * 10) + (numeric_coord - ascii0)


def transform_horizontal(value):
    return mapvalue(to_numeric(value), to_numeric(leftCoord), to_numeric(rightCoord), leftGPS, rightGPS)


# Turns a string of the form [A-Z][0-9][0-9][0-9] into GPS coordinates.
def transform_point(coords):
    if len(coords) > 4:
        coords = coords[2:6]
    tens_coord = ord(coords[2])
    ones_coord = ord(coords[3])
    vertical_coord = transform_vertical(((tens_coord - ascii0) * 10) + (ones_coord - ascii0))
    horizontal_coord = transform_horizontal(coords[0:2])
    return [vertical_coord, horizontal_coord]


def test():
    print('transform top: ' + str(transform_vertical(top_coord)))
    print('transform bottom: ' + str(transform_vertical(bottom_coord)))
    print('transform left: ' + str(transform_horizontal(leftCoord)))
    print('transform right: ' + str(transform_horizontal(rightCoord)))
    print('transform upper left: ' + str(transform_point(leftCoord + '18')))
    print('transform lower right: ' + str(transform_point(rightCoord + '46')))
    print('transform lower right: ' + str(transform_point('99' + rightCoord + '46')))
    print('transform test data 1: ' + str(transform_point('D625')))


def main():
    pass


if '__main__' == __name__:
    main()
    # test()
