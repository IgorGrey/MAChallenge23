### PSEDUO CODE ###
#precondition - boat are moving towards the plume and will enter in by exceeding minimum threshold
#Set threshold for pollution sensor readings

#list1 = []
#list 2 = []
#same_turn_count = int
#turn_direction = int (1 for left 2 for right)

#-read in SIG every second
#- once entered the pollution area
#- save SIG and current GPS loc to "Vertical" and "Horizontal" lists depending on how many turns done if any (if none or 2 write to Vertical if 1 or 3 to horizontal)
#TODO: Check 3 main scenarios for clearing the lists properly depending on how many turns done
#- current reading < threshold = exited plume
#- make 90 degree turn (right or left - any)
#TODO: MAYBE! reduce x-track error
#-- if no increase of SIG repeat step 4
#--- if turned same way twice = reverse turn direction step 4
#---- if turned same way 3 times reverse turn direction in step 4
#TODO: MAYBE! Reduce stame_turn_count from 4 to 3 and from 2 to 1 to optimize algo

#- repeat 1-4

#Every time after exiting plume if both lists (vertical and horizontal) "filled" following code block will run:tttt

#- pick 2 strongest pollution values from vertical and horizontal lists and using gps loc predict epicentre
#- set heading towards approx. epicentre as a heading
#- repeat 1-7 within strongest values area (as if they were 0)
#- SUCCESS CONDITION  = readin 80-90% pollution!

# ADD LOGIC TO STAY IN EPICENTRE IF POLLUTION THRESHOLD > 80 

#Potential improvement:
#Normalize last 3 pollution readings for last 3 sec, to protect from spikes. add empty list, low values error handlers


#Normalize the heading value to a value between 0 and 360

import generate_thd_hsc
import main1
import socket
import ports_module
import threading
import pynmea2
from datetime import datetime
import generate_thd_hsc
import distanceFormula
import headingStandalone
import main1
import json
import ChalFOURfunctions

def calculate_within_360(value):
    value %= 360  # Calculate remainder
    if value < 0:
        value += 360  # Adjust negative values
    return value
# Example usage
# initial_value = 450
# result = calculate_within_360(initial_value)
# print(result)  # Output: 90

# GPS format coverter fundtion DDM to DD
def ddm_to_decimal(ddm):
    # Convert DDM (Degrees Decimal Minutes) coordinates to decimal degrees
    degrees = int(ddm) // 100  # Extract the degrees component
    minutes = (int(ddm) % 100) / 60  # Extract the minutes component and convert to decimal
    decimal = degrees + minutes  # Combine degrees and decimal minutes
    return decimal

# Returns gps location of forth corner of the square, from given 3 gps locations
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

# EXAMPLE Call the calculate_fourth_corner function with DDM coordinates as parameters
# lat_fourth, long_fourth = calculate_fourth_corner(-0.209766874, -0.403398735, 0.693828867, 0.419534685, 0.718030954, 0.952021015)
# Print the results
# print("Latitude of the fourth corner:", lat_fourth)
# print("Longitude of the fourth corner:", long_fourth)

# main logic
threshold = 20  # Set threshold for pollution sensor readings
vertical_list = []
horizontal_list = []
# NEED => to check when to reset back to 0 <= 
same_turn_count = 0
turn_direction = -1  # -1 for left, 1 for right

#def read_sensor_data():
    # Code to read SIG value every second
    #return sig_value, gps_location