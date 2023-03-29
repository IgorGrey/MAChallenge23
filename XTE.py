import math

def calculate_cte(current_pos, previous_pos, desired_pos):
    """
    Calculate the cross-track error (CTE) between the current position and the desired position
    based on the previous position.

    Args:
        current_pos (tuple): A tuple containing the current position in the format (latitude, longitude).
        previous_pos (tuple): A tuple containing the previous position in the format (latitude, longitude).
        desired_pos (tuple): A tuple containing the desired position in the format (latitude, longitude).

    Returns:
        float: The cross-track error in meters.
    """

    # Convert coordinates to radians
    current_lat, current_lon = math.radians(current_pos[0]), math.radians(current_pos[1])
    previous_lat, previous_lon = math.radians(previous_pos[0]), math.radians(previous_pos[1])
    desired_lat, desired_lon = math.radians(desired_pos[0]), math.radians(desired_pos[1])

    # Calculate the distance and initial bearing from the previous position to the current position
    distance = math.acos(math.sin(previous_lat) * math.sin(current_lat) +
                         math.cos(previous_lat) * math.cos(current_lat) * math.cos(current_lon - previous_lon)) * 6371000  # Earth's radius in meters
    initial_bearing = math.atan2(math.sin(current_lon - previous_lon) * math.cos(current_lat),
                                 math.cos(previous_lat) * math.sin(current_lat) - math.sin(previous_lat) * math.cos(current_lat) * math.cos(current_lon - previous_lon))

    # Calculate the distance and bearing from the previous position to the desired position
    desired_distance = math.acos(math.sin(previous_lat) * math.sin(desired_lat) +
                                 math.cos(previous_lat) * math.cos(desired_lat) * math.cos(desired_lon - previous_lon)) * 6371000  # Earth's radius in meters
    desired_bearing = math.atan2(math.sin(desired_lon - previous_lon) * math.cos(desired_lat),
                                 math.cos(previous_lat) * math.sin(desired_lat) - math.sin(previous_lat) * math.cos(desired_lat) * math.cos(desired_lon - previous_lon))

    # Calculate the cross-track error
    cte = math.asin(math.sin(distance / 6371000) * math.sin(initial_bearing - desired_bearing)) * 6371000

    # return cte
    return print(cte)

current_pos = (37.7754, -122.4194)
previous_pos = (37.7750, -122.4189)
desired_pos = (37.7755, -122.4195)
calculate_cte(current_pos, previous_pos,desired_pos)