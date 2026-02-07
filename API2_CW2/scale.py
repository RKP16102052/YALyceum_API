def get_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]

    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    dx = abs(float(upper_corner[0]) - float(lower_corner[0]))
    dy = abs(float(upper_corner[1]) - float(lower_corner[1]))

    return dx, dy
