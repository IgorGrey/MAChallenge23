def ddm_to_decimal(ddm):
    # Convert DDM (Degrees Decimal Minutes) coordinates to decimal degrees
    degrees = int(ddm) // 100  # Extract the degrees component
    minutes = (int(ddm) % 100) / 60  # Extract the minutes component and convert to decimal
    decimal = degrees + minutes  # Combine degrees and decimal minutes
    return decimal

def calculate_fourth_corner(lat1, long1, lat2, long2, lat3, long3):
    # Convert DDM coordinates to decimal degrees
    lat1_decimal = ddm_to_decimal(lat1)
    long1_decimal = ddm_to_decimal(long1)
    lat2_decimal = ddm_to_decimal(lat2)
    long2_decimal = ddm_to_decimal(long2)
    lat3_decimal = ddm_to_decimal(lat3)
    long3_decimal = ddm_to_decimal(long3)

    # Calculate the average latitude and longitude
    lat_avg = (lat1_decimal + lat2_decimal + lat3_decimal) / 3
    long_avg = (long1_decimal + long2_decimal + long3_decimal) / 3

    # Calculate the relative distance from the center to one of the corners
    lat_diff = lat1_decimal - lat_avg
    long_diff = long1_decimal - long_avg

    # Calculate the GPS location of the fourth corner
    lat_fourth = lat_avg + lat_diff
    long_fourth = long_avg + long_diff

    return lat_fourth, long_fourth

# Call the calculate_fourth_corner function with DDM coordinates as parameters
lat_fourth, long_fourth = calculate_fourth_corner(-0.209766874, -0.403398735, 0.693828867, 0.419534685, 0.718030954, 0.952021015)

# Print the results
print("Latitude of the fourth corner:", lat_fourth)
print("Longitude of the fourth corner:", long_fourth)
