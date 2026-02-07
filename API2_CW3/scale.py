def get_spn_for_two_points(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])

    return dx * 1.5, dy * 1.5
