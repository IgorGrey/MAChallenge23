def convert_minutes_to_degrees(lat1):
    number = lat1
    minutes = str(number - int(number))[1:]
    minutes = float(minutes) * 100
    degrees = str(number)[:2]
    degrees1 = int(degrees)
    # Calculate the degrees from the integer part of the minutes
    degrees = int(minutes / 60)

    # Calculate the remaining minutes
    remaining_minutes = minutes % 60

    # Calculate the decimal representation of the remaining minutes
    decimal_minutes = remaining_minutes / 60.0

    # Calculate the total degrees
    total_degrees = degrees1 + decimal_minutes


    return round(total_degrees,3)

