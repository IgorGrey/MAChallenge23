


#Normalize the heading value to a value between 0 and 360
def calculate_within_360(value):
    value %= 360  # Calculate remainder
    if value < 0:
        value += 360  # Adjust negative values
    return value
  


# Example usage
# initial_value = 450
# result = calculate_within_360(initial_value)
# print(result)  # Output: 90
