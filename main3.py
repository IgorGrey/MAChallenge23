import math 
import distanceFormula
import main1
import ports_module
import main4_old
def autonomously_berth(start_latitude, start_longitude, berthing_points, heading):
    safety_distance = 1.0  # meters
    parallel_threshold = 5.0  # degrees

    for berthing_point in berthing_points:
        target_latitude, target_longitude = berthing_point
        distance_to_target = distanceFormula.calculate_distance  (start_latitude, start_longitude, target_latitude, target_longitude)
        print(f"Starting Distance to Target: {distance_to_target:.2f} meters")

        while distance_to_target > safety_distance:
            # Calculate the bearing from start to target
            dlat = math.radians(target_latitude - start_latitude)
            dlon = math.radians(target_longitude - start_longitude)
            y = math.sin(dlon) * math.cos(math.radians(target_latitude))
            x = math.cos(math.radians(start_latitude)) * math.sin(math.radians(target_latitude)) - \
                math.sin(math.radians(start_latitude)) * math.cos(math.radians(target_latitude)) * math.cos(dlon)
            bearing = math.degrees(math.atan2(y, x))
            if bearing < 0:
                bearing += 360

            # Simulate movement towards the target
            movement_distance = 10.0  # meters
            start_latitude += (movement_distance / 1000) * math.cos(math.radians(bearing))
            start_longitude += (movement_distance / 1000) * math.sin(math.radians(bearing))

            # Recalculate the distance to the target
            distance_to_target = distanceFormula.calculate_distance(start_latitude, start_longitude, target_latitude, target_longitude)
            print(f"Current Distance to Target: {distance_to_target:.2f} meters")

        # Check if the USV has parallelly berthed
        bearing_to_target = heading # HSC reading !!!!!!!!!!!!!!!!!!!
        if abs(bearing_to_target) < parallel_threshold or abs(bearing_to_target - 180) < parallel_threshold:
            print("Successful berthing! The USV is fully stopped in parallel to the berth.")
        else:
            print("Berthing failed. The USV is not parallel to the berth.")

        # Update the start position for the next berthing point
        start_latitude = target_latitude
        start_longitude = target_longitude




def start_program(_online_port):
    list_of_ports = ports_module.check_ports()
    

    loop_keep_alive = True

    while loop_keep_alive:
        res = _online_port.readline().decode()
        if res and res.startswith("$"+"GPRMC"):
        # list of 4 arguments i need only 0 and 2 lat and lon
            current_location = main4_old.get_location_coordinates(res)
            # Specify the start point coordinates # GET REAL DATA FROM RMC sentences 
            start_latitude = float(current_location[0])
            start_longitude = float(current_location[2])
            heading = main4_old.get_heading_degrees(res)

            autonomously_berth(start_latitude, start_longitude, berthing_points, heading)
    



# Specify the berthing points as a list of tuples (latitude, longitude)
berthing_points = [
    
(-1.49563959,	51.01500392),
(-1.49587255,	51.01491172),
(-1.49531816,	51.01499806),
(-1.49542321,	51.01508828),
(-1.49523361,	51.01502972),
(-1.49523365,	51.01502975),
(-1.49512412,	51.01511353),
(-1.49522565,	51.01515629),
(-1.49631525,	51.01482022),
(-1.4963771,    51.01478376),
(-1.49633863,	51.01475266),
(-1.49645447,	51.01467527),
(-1.49645579,	51.01467632),
(-1.49628293,	51.01455707),
(-1.49608418,	51.01444152),
(-1.49622863,	51.01451692),
(-1.49558683,	51.01506076),
(-1.49555635,	51.01501464),
(-1.49552099,	51.01498482),
(-1.49548965,	51.01496168),
(-1.49546532,	51.01494964),
(-1.49543341,	51.01494439),
(-1.49541201,	51.01495155),
(-1.49539038,	51.014962),
(-1.49539189,	51.01497994),
(-1.49539464,	51.01499952),
(-1.49540872,	51.01502126),
(-1.49541658,	51.01503946),
(-1.49543392,	51.01505525),
(-1.49547898,	51.01509668),
(-1.49512372,	51.0142176),
(-1.49495033,	51.014267),
(-1.49495557,	51.01427317),
(-1.49498072,	51.01426694),
(-1.49500674,	51.01425966),
(-1.49503336,	51.01425163),
(-1.49506038,	51.01424457),
(-1.49506204,	51.01424418),
(-1.49506204,	51.01424418),
(-1.49506204,	51.01424418),
(-1.49506204,	51.01424418),
(-1.49506204,	51.01424418),
(-1.49400791,	51.01466578),
(-1.49391204,	51.0145692),
(-1.49391904,	51.01456555),
(-1.4939344,    51.01457934),
(-1.49395344,	51.01459873),
(-1.49397199,	51.01461722),
(-1.49398971,	51.01463458),
(-1.49400751,	51.01464975),
(-1.49402074,	51.01466293),
(-1.49402932,	51.01467101),
(-1.49401737,	51.01467696),
(-1.49400363,	51.01466426),
(-1.49399335,	51.01465369),
(-1.49398332,	51.01464308),
(-1.49397399,	51.01463419),
(-1.49396417,	51.0146237),
(-1.49395317,	51.01461282),
(-1.4939444,   51.01460173),
(-1.49393429,	51.01459017),
(-1.49392301,	51.01457981),
]
    # Add more berthing points as needed
if __name__ == "__main__":
    start_program(ports_module.connect_to_port("COM5"))