# Transform from 1980 paper map coordinates to GPS

def map(value, fromStart, fromEnd, toStart, toEnd):
    if (fromEnd == fromStart):
        return value
    return (value - fromStart) * (toEnd - toStart) / (fromEnd - fromStart) + toStart;

# Gotten from manually observing existing data
topCoord = 18
bottomCoord = 46
topGPS = 37.73595
bottomGPS = 37.70097

def transformVertical(value):   
    return map(value, topCoord, bottomCoord, topGPS, bottomGPS)

leftCoord = 'B7'
rightCoord = 'E9'
leftGPS = -122.19608
rightGPS = -122.12383

asciiA = ord('A')
ascii0 = ord('0')

# Turns a string of the form [A-Z][0-9] into a number between 0 and whatever.
def toNumeric(coord):
    alphaCoord = ord(coord[0])
    numericCoord = ord(coord[1])
    return ((alphaCoord - asciiA) * 10) + (numericCoord - ascii0)

def transformHorizontal(value):
    return map(toNumeric(value), toNumeric(leftCoord), toNumeric(rightCoord), leftGPS, rightGPS)

# Turns a string of the form [A-Z][0-9][0-9][0-9] into GPS coordinates.
def transformPoint(coords):
    if (len(coords) > 4):
        coords = coords[2:6]
    tensCoord = ord(coords[2])
    onesCoord = ord(coords[3])
    verticalCoord = transformVertical(((tensCoord - ascii0) * 10) + (onesCoord - ascii0))
    horizontalCoord = transformHorizontal(coords[0:2])
    return [verticalCoord, horizontalCoord]

def test():
    print('transform top: ' + str(transformVertical(topCoord)))
    print('transform bottom: ' + str(transformVertical(bottomCoord)))
    print('transform left: ' + str(transformHorizontal(leftCoord)))
    print('transform right: ' + str(transformHorizontal(rightCoord)))
    print('transform upper left: ' + str(transformPoint(leftCoord + '18')))
    print('transform lower right: ' + str(transformPoint(rightCoord + '46')))
    print('transform lower right: ' + str(transformPoint('99' + rightCoord + '46')))
    print('transform test data 1: ' + str(transformPoint('D625')))

test()
