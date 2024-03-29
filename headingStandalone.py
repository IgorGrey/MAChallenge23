import math

def convert_gps_format(gps_format):
    """
    Converts GPS coordinates from degree and decimal minute format to decimal degree format.
    Example: 5050.710799,N -> 50.84517998333333
    """
    degrees = float(gps_format[:2])
    minutes = float(gps_format[2:])
    decimal_degrees = degrees + (minutes / 60.0)
    return round(decimal_degrees, 7)

def extract_lat_lon(nmea_sentence):
    """
    Extracts latitude and longitude from a GPRMC NMEA sentence.
    Example: $GPRMC,001115.81,A,5050.700849,N,00044.822914,W,0.0,269.7,230418,4.0,W,A,S*43
    """
    lat = 0.0
    lon = 0.0
    if nmea_sentence.find("GPRMC") > 0:
        data = nmea_sentence.split(",")
        lat = convert_gps_format(data[3])
        if data[4] == "S":
            lat = -lat
        lon = convert_gps_format(data[5])
        if data[6] == "W":
            lon = -lon
    return round(lat, 6), round(lon, 6)

def extract_lat_lon_from_wpl(nmea_sentence):
    """
    Extracts latitude and longitude from a MMWPL NMEA sentence.
    Example: $MMWPL,5050.710799,N,00044.755897,W,WPT 1*73
    """
    lat = 0.0
    lon = 0.0
    if nmea_sentence.find("MMWPL") > 0:
        data = nmea_sentence.split(",")
        lat = convert_gps_format(data[1])
        if data[2] == "S":
            lat = -lat
        lon = convert_gps_format(data[3])
        if data[4] == "W":
            lon = -lon
    return round(lat, 6), round(lon, 6)

def calculate_heading(current_lat, current_lon, target_lat, target_lon):
    """
    Calculates the heading from the current GPS position to the target GPS position.
    """
    current_lat_rad = math.radians(current_lat)
    current_lon_rad = math.radians(current_lon)
    target_lat_rad = math.radians(target_lat)
    target_lon_rad = math.radians(target_lon)
    
    delta_lon_rad = target_lon_rad - current_lon_rad
    
    y = math.sin(delta_lon_rad) * math.cos(target_lat_rad)
    x = (math.cos(current_lat_rad) * math.sin(target_lat_rad)) - \
        (math.sin(current_lat_rad) * math.cos(target_lat_rad) * math.cos(delta_lon_rad))
    
    heading_rad = math.atan2(y, x)
    heading_deg = math.degrees(heading_rad)
    if heading_deg < 0:
        heading_deg += 360
    
    return heading_deg

# Example usage
nmea_sentence = "$MMWPL,5050.710799,N,00044.755897,W,WPT 1*73"
current_lat, current_lon = 50.845000, -0.746217
target_lat, target_lon = extract_lat_lon_from_wpl(nmea_sentence)
print(target_lat,target_lon)
heading = calculate_heading(target_lat, target_lon, current_lat, current_lon)
print(f"Heading: {heading:.2f} degrees")
