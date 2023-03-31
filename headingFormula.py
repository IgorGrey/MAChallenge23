import math

def calculate_heading(lat2, lon2, lat1, lon1):
    # Convert latitude and longitude to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate the difference in longitude
    delta_lon = lon2 - lon1
    print(lon1, lon2, delta_lon)

    # Calculate the heading angle using the formula
    y = math.sin(delta_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    heading = math.atan2(y, x)
    heading = math.degrees(heading)
    print(heading)
    print(x,y)

    # Normalize the heading angle to a value between 0 and 360 degrees
    if heading < 0:
        heading += 360

    return heading

# Test the function with the provided GPS coordinates
#lat1 = 50.70000000
#lon1 = 0.44773000
#lat2 = 50.50710799
#lon2 = 0.44755897
#heading = calculate_heading(lat2, lon2, lat1, lon1)
#print("Heading: {:.1f} degrees".format(heading))
