# transform from map coordinates to GPS

def map(value, fromStart, fromEnd, toStart, toEnd):
    if (fromEnd == fromStart):
        return value
    return (value - fromStart) * (toEnd - toStart) / (fromEnd - fromStart) + toStart;

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

def toNumeric(coord):
    asciiA = ord('A')
    alphaCoord = ord(coord[0])
    ascii0 = ord('0')
    numericCoord = ord(coord[1])
    return ((alphaCoord - asciiA) * 10) + (numericCoord - ascii0)

def transformHorizontal(value):
    return map(toNumeric(value), toNumeric(leftCoord), toNumeric(rightCoord), leftGPS, rightGPS)

def test():
    print('transform top: ' + str(transformVertical(topCoord)))
    print('transform bottom: ' + str(transformVertical(bottomCoord)))
    print('transform left: ' + str(transformHorizontal(leftCoord)))
    print('transform right: ' + str(transformHorizontal(rightCoord)))

test()
