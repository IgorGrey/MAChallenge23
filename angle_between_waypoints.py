import math
# NOT WORKING VERSION, NEEDS PARAMETERS CHANGED
def angle_between_waypoints(coords):
    # Convert the coordinates to radians
    coords = [(math.radians(float(lat)), math.radians(float(lon))) for (lat, lon) in coords]
    
    # Calculate the vectors between the waypoints
    v1 = (coords[0][0] - coords[1][0], coords[0][1] - coords[1][1])
    v2 = (coords[2][0] - coords[1][0], coords[2][1] - coords[1][1])
    
    # Calculate the dot product and the magnitudes of the vectors
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Calculate the angle between the vectors
    angle = math.ceil(math.degrees(math.acos(dot_product / (mag_v1 * mag_v2))))
    
    return angle
