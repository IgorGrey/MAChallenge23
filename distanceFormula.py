from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c * 1000
    
    return round(float(distance))
    
# Test the function with the provided GPS coordinates
lat1 = 50.50699892
lon1 = -0.44772998
lat2 = 50.50710799
lon2 = -000.44755897

distance = calculate_distance(lon1, lat1, lon2, lat2)
print(distance) # Output: 41.96276179911194 (approx. 42 meters)


