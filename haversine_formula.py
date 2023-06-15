import math

def calulate_new_coords(lat, lon, bearing, distance, offset):
    lat_deg = int(lat / 100)
    lat_min = lat % 100
    lat = lat_deg + lat_min / 60

    lon_deg = int(lon / 100)
    lon_min = lon % 100
    lon = lon_deg + lon_min / 60

    lat = math.radians(lat)
    lon = math.radians(lon)

    bearing = math.radians(bearing)
    radius = 3440.1

    distance = (distance * 1852 + offset) / (radius * 1852)

    new_lat = math.asin(math.sin(lat) * math.cos(distance) +
                        math.cos(lat) * math.sin(distance) * math.cos(bearing))

    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance) * math.cos(lat),
                                math.cos(distance) - math.sin(lat) * math.sin(new_lat))

    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    new_lat_deg = int(new_lat)
    new_lat_min = (new_lat - new_lat_deg) * 60
    new_lat = new_lat_deg * 100 + new_lat_min

    new_lon_deg = int(new_lon)
    new_lon_min = (new_lon - new_lon_deg) * 60
    new_lon = new_lon_deg * 100 + new_lon_min

    return new_lat, new_lon

def deg_to_decimal_deg(degrees, minutes):
    return degrees + minutes / 60

def calucate_new_waypoint(lat, lon, bearing, distance):
    new_bearing = (bearing + 90) % 360

    waypoint_lat, waypoint_lon = calulate_new_coords(lat, lon, new_bearing, distance)

    return waypoint_lat, waypoint_lon