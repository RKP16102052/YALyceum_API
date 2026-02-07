def get_spn_for_points(points):
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]

    dx = max(lats) - min(lats)
    dy = max(lons) - min(lons)

    return dx * 1.3, dy * 1.3
