import math

def calulate_new_coords(lat, lon, bearing, distance):
    lat = math.radians(lat)
    lon = math.radians(lon)

    bearing = math.radians(bearing)
    radius = 3440.1

    new_lat = math.asin(math.sin(lat) * math.cos(distance) +
                        math.cos(lat) * math.sin(distance) * math.cos(bearing))

    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance) * math.cos(lat),
                                math.cos(distance) - math.sin(lat) * math.sin(new_lat))

    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return new_lat, new_lon

def deg_to_decimal_deg(degrees, minutes):
    return degrees + minutes / 60

def calucate_new_waypoint(lat, lon, bearing, distance):
    new_bearing = (bearing + 90) % 360

    waypoint_lat, waypoint_lon = calulate_new_coords(lat, lon, new_bearing, distance)

    return waypoint_lat, waypoint_lon