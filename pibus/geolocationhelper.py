from math import radians, sin, cos, atan2, sqrt

# Haversine formula for calculating short distances
def distance_between(lat1, long1, lat2, long2):
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    delta_lat = lat2 - lat1
    delat_long = long2 - long1

    a = (sin(delta_lat / 2))^2 + cos(lat1) * cos(lat2) * (sin(delta_long / 2))^2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6373 # radius of the Earth in km
    distance = R * c
    return distance
