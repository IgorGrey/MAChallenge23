import socket
import threading
import generate_thd_hsc
import headingStandalone
import json
import math 
import main1
import ports_module


with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)


def send_cmd_to_system(cmd):
    _online_port = ports_module.connect_to_port(config["general"]["input_port"])
    _online_port.write(cmd)
    res = _online_port.readline().decode()
    print(res)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_location_coordinates(rmc_cmd):
    sentence = rmc_cmd.split(",")

    # Make sure the command is GPRMC
    if sentence[0] == "$GPRMC":
        # degrees, N or S, degrees, W or E, heading
        return [sentence[3], sentence[4], sentence[5], sentence[6], sentence[8]]
    else:
        return 0

# def autonomously_berth(start_latitude, start_longitude, berthing_points, heading):
#     safety_distance = 1.0  # meters
#     parallel_threshold = 5.0  # degrees

#     for berthing_point in berthing_points:
#         target_latitude, target_longitude = berthing_point
#         distance_to_target = distanceFormula.calculate_distance  (start_latitude, start_longitude, target_latitude, target_longitude)
#         print(f"Starting Distance to Target: {distance_to_target:.2f} meters")

#         while distance_to_target > safety_distance:
#             # Calculate the bearing from start to target
#             dlat = math.radians(target_latitude - start_latitude)
#             dlon = math.radians(target_longitude - start_longitude)
#             y = math.sin(dlon) * math.cos(math.radians(target_latitude))
#             x = math.cos(math.radians(start_latitude)) * math.sin(math.radians(target_latitude)) - \
#                 math.sin(math.radians(start_latitude)) * math.cos(math.radians(target_latitude)) * math.cos(dlon)
#             bearing = math.degrees(math.atan2(y, x))
#             if bearing < 0:
#                 bearing += 360

#             # Simulate movement towards the target
#             movement_distance = 10.0  # meters
#             start_latitude += (movement_distance / 1000) * math.cos(math.radians(bearing))
#             start_longitude += (movement_distance / 1000) * math.sin(math.radians(bearing))

#             # Recalculate the distance to the target
#             distance_to_target = distanceFormula.calculate_distance(start_latitude, start_longitude, target_latitude, target_longitude)
#             print(f"Current Distance to Target: {distance_to_target:.2f} meters")

#         # Check if the USV has parallelly berthed
#         bearing_to_target = heading # HSC reading !!!!!!!!!!!!!!!!!!!
#         if abs(bearing_to_target) < parallel_threshold or abs(bearing_to_target - 180) < parallel_threshold:
#             print("Successful berthing! The USV is fully stopped in parallel to the berth.")
#         else:
#             print("Berthing failed. The USV is not parallel to the berth.")

#         Update the start position for the next berthing point
#         start_latitude = target_latitude
#         start_longitude = target_longitude

safeAreaWpnts = [
 (-1.4949756,	 51.0145927)
 (-1.4947917,	 51.0150555)
 (-1.4952066,	 51.0148913)
 (-1.4951342,	 51.0149263)
 (-1.4950497,	 51.0149643)
 (-1.4953945,	 51.0145467)
 (-1.4956263,	 51.0146539)
 (-1.495377,	 51.0148528)
 (-1.4944199,	 51.0148934)]

all_berth_data = [["Berth 1-1",(-1.4956263, 51.0146539),(-1.4958094, 51.0147379),(-1.495965, 51.0148468),(-1.4956327, 51.0149771)],
["Berth 1-2",(-1.4956263, 51.0146539),(-1.4958094, 51.0147379),(-1.495965, 51.0148468),(-1.4958506, 51.0148919)],
["Berth 2-1",(-1.4951342, 51.0149263),(-1.4952198, 51.0149517),(-1.4952768, 51.0149838),(-1.4953036, 51.0150033)],
["Berth 2-2",(-1.4951342, 51.0149263),(-1.4952198, 51.0149517),(-1.4952768, 51.0149838),(-1.4954028, 51.0150952)],
["Berth 3-1",(-1.4950497, 51.0149643),(-1.4951165, 51.0149884),(-1.4951896, 51.0150163),(-1.4952169, 51.015037)],
["Berth 3-2",(-1.4950497, 51.0149643),(-1.4951165, 51.0149884),(-1.4951896, 51.0150163),(-1.4952169, 51.015037)],
["Berth 4-1",(-1.4947917, 51.0150555),(-1.4949127, 51.0150719),(-1.4950508, 51.0150973),(-1.4951144, 51.0151223)],
["Berth 4-2",(-1.4947917, 51.0150555),(-1.4949127, 51.0150719),(-1.4950508, 51.0150973),(-1.4952123, 51.0151657)],
["Berth 21-1",(-1.4956263, 51.0146539),(-1.495804, 51.0146387),(-1.4962184, 51.0147028),(-1.4963143, 51.0148147)],
["Berth 21-2",(-1.4956263, 51.0146539),(-1.495804, 51.0146387),(-1.4962184, 51.0147028),(-1.4963632, 51.0147856)],
["Berth 21-3",(-1.4956263, 51.0146539),(-1.495804, 51.0146387),(-1.4962184, 51.0147028),(-1.4963257, 51.0147603)],
["Berth 21-4",(-1.4953945, 51.0145467),(-1.4955573, 51.0144548),(-1.4959529, 51.0144185),(-1.4964427, 51.0146786)],
["Berth 20-1",(-1.4953945, 51.0145467),(-1.4955573, 51.0144548),(-1.4959529, 51.0144185),(-1.4964427, 51.0146786)],
["Berth 20-2",(-1.4953945, 51.0145467),(-1.4955573, 51.0144548),(-1.4959529, 51.0144185),(-1.4962697, 51.0145609)],
["Berth 19-1",(-1.4953945, 51.0145467),(-1.4955573, 51.0144548),(-1.4959529, 51.0144185),(-1.4960689, 51.014447)],
["Berth 19-2",(-1.4953945, 51.0145467),(-1.4955573, 51.0144548),(-1.4959529, 51.0144185),(-1.4962144, 51.0145212)],
["Grass island-1",(-1.495377, 51.0148528),(-1.4954242, 51.0148783),(-1.4954718, 51.0149057),(-1.4956031, 51.0149824)],
["Grass island-2",(-1.495377, 51.0148528),(-1.4954242, 51.0148783),(-1.4954718, 51.0149057),(-1.4956031, 51.0149824)],
["Grass island-3",(-1.495377, 51.0148528),(-1.4954242, 51.0148783),(-1.4954718, 51.0149057),(-1.4955789, 51.0149634)],
["Grass island-4",(-1.495377, 51.0148528),(-1.4954242, 51.0148783),(-1.4954718, 51.0149057),(-1.495538, 51.0149414)],
["Grass island-5",(-1.495377, 51.0148528),(-1.4954242, 51.0148783),(-1.4954718, 51.0149057),(-1.4954931, 51.0149216)],
["Grass island-6",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4954213, 51.0149199)],
["Grass island-7",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4953945, 51.0149326)],
["Grass island-8",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.495369, 51.0149592)],
["Grass island-9",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4953717, 51.0149807)],
["Grass island-10",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4953717, 51.0149807)],
["Grass island-11",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4953925, 51.015022)],
["Grass island-12",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.4954052, 51.0150402)],
["Grass island-13",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.495422, 51.0150579)],
["Grass island-14",(-1.4952066, 51.0148913),(-1.4952714, 51.0149154),(-1.4953324, 51.0149412),(-1.495422, 51.0150579)],
["Berth 18-1",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4951325, 51.0142335)],
["Berth 18-2",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950084, 51.0142664)],
["Berth 18-3",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4949517, 51.0142822)],
["Berth 18-1",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4951325, 51.0142335)],
["Berth 18-2",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950084, 51.0142664)],
["Berth 18-3",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4949517, 51.0142822)],
["Berth 18-4",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 18-5",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 18-6",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 18-7",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 18-8",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 18-9",(-1.4949756, 51.0145927),(-1.4949289, 51.0144646),(-1.4948789, 51.0143102),(-1.4950688, 51.0142454)],
["Berth 17-1",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939926, 51.0146727)],
["Berth 17-2",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.493896, 51.0145756)],
["Berth 17-3",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4939362, 51.0145672)],
["Berth 17-4",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4939503, 51.0145777)],
["Berth 17-5",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4939691, 51.0145976)],
["berth 17-6",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4939892, 51.0146157)],
["Berth 17-7",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4940073, 51.0146326)],
["Berth 17-8",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4940214, 51.014649)],
["Berth 17-9",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4940341, 51.01466)],
["Berth 17-10",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940946, 51.0147242),(-1.4940429, 51.014668)],
["Berth 17-11",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.494004, 51.0146819)],
["Berth 17-12",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939879, 51.0146706)],
["Berth 17-13",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939792, 51.01466)],
["Berth 17-14",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939691, 51.0146473)],
["Berth 17-15",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939597, 51.0146376)],
["Berth 17-16",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939503, 51.0146288)],
["Berth 17-17",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939396, 51.0146174)],
["Berth 17-18",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939302, 51.0146068)],
["Berth 17-19",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939195, 51.0145955)],
["Berth 17-20",(-1.4944199, 51.0148934),(-1.4943011, 51.0148106),(-1.4940577, 51.014733),(-1.4939067, 51.0145849)]]

chosen_berth = [] # [berth_name, save_wpnt, wpnt1, wpnt2, wpnt3]
middleWpntSafeArea = [(-1.4953089, 51.0147121), (-1.4949817, 51.0148386), (-1.4947268, 51.0149517)]
actuallyClosestSafeWpnt = []
recommended_speed = config["chal3"]["l0_speed"] # GRAB FROM CONFIG AND ASSING TO THIS VAR, USED LATER
#----------------------------------------------------------------------------

given_berth_name = "Berth 1-1" # GIVEN BY ORGANISIRES! ENTER WITH CAUTION, USE CAPITAL FIRST LETTER!

#-----------------------------------------------------------------------------------------

def rads_jebany_function(rmc_cmd):
    closestSafeAreaWpnts = [] # [[meters, lon, lat]] 
    for safeAreaWpnt in safeAreaWpnts:
        m = headingStandalone.calc_distance(rmc_cmd[0], rmc_cmd[2], safeAreaWpnt[1], safeAreaWpnt[0]) # or safeAreaWpnt[0],safeAreaWpnt[1]
        closestSafeAreaWpnts.append(m,safeAreaWpnt[0],safeAreaWpnt[1])
    actuallyClosestSafeWpnt = min(closestSafeAreaWpnts) # [meters,lon,lat]
    
    closestMiddleSafeAreaWpnts = [] # [[meters, lat, lon]]
    for wpnt in middleWpntSafeArea:
        w = headingStandalone.calc_distance(rmc_cmd[0], rmc_cmd[2], wpnt[1], wpnt[0]) # or  wpnt[0], wpnt[1]
        closestMiddleSafeAreaWpnts.append(w, wpnt[0], wpnt[1])
    actuallyMiddleClosestSafeWpnt = min(closestMiddleSafeAreaWpnts)

    a = headingStandalone.calc_distance(rmc_cmd[0], rmc_cmd[2],actuallyClosestSafeWpnt[2], actuallyClosestSafeWpnt[1])
    b = headingStandalone.calc_dinstance(rmc_cmd[0], rmc_cmd[2],actuallyMiddleClosestSafeWpnt[2], actuallyMiddleClosestSafeWpnt[1])
    if a <= b: # if condition met heading to safe area, if not assume we are in safe area and while loop takes over
        
        h = headingStandalone.calc_heading(rmc_cmd[0], rmc_cmd[2], actuallyClosestSafeWpnt[2], actuallyClosestSafeWpnt[1])  
        # After calculating heading, send it to the system as HSC
        hsc_sentence = generate_thd_hsc.generate_hsc_sentence(h)
        hsc_sentence = hsc_sentence + "*" + main1.calculate_checksum(hsc_sentence[1:])
        hsc_sentence = hsc_sentence + "\r\n"
        hsc_sentence = hsc_sentence.encode("ascii")
        print(hsc_sentence)
        send_cmd_to_system(hsc_sentence)
        
    distance =  0 # used for while loop
    # repeats for every time var actuallyClosestSafeWpnt is updated and distance to it less then 5m
    i = 1 
    while i < 4: # outside safe area scenario
        distance = distanceFormula.calc_distance(rmc_cmd[0], rmc_cmd[2], actuallyClosestSafeWpnt[2], actuallyClosestSafeWpnt[1])
        if distance < 5:
            # Stage 2: get to clothest beth safe location
            if chosen_berth == "": # runs once
                for beth in all_berth_data: # search in all_berth_data for record with string matching given_berth_name ---- "Berth 1-1" -example
                    if given_berth_name == berth[0]:
                    chosen_berth = berth
            actuallyClosestSafeWpnt = [0,chosen_berth[i+1], chosen_berth[i]]  # [meters, lon, lat] --- updates actuallyClosestSafeWpnt to follow on next iterration of the loop
            new_h = headingStandalone.calc_heading(rmc_cmd[0], rmc_cmd[2], actuallyClosestSafeWpnt[2], actuallyClosestSafeWpnt[1]) # send boat to HDG towards updated actuallyClosestSafeWpnt
            
            hsc_sentence = generate_thd_hsc.generate_hsc_sentence(new_h)
            hsc_sentence = hsc_sentence + "*" + main1.calculate_checksum(hsc_sentence[1:])
            hsc_sentence = hsc_sentence + "\r\n"
            hsc_sentence = hsc_sentence.encode("ascii")
            print(hsc_sentence)
            send_cmd_to_system(hsc_sentence)     #generate_thc_sentence() ------  OR  ------------ _online_port.write(thc_cmd)   
    
            new_speed = recommended_speed - (i * 2)   # updates global var, speed reduction every leg of the track

            thd_cmd = generate_thd_hsc.generate_thd_sentence(new_speed)
            thd_cmd = thd_cmd + "*" + main1.calculate_checksum(thd_cmd[1:])
            thd_cmd = thd_cmd + "\r\n"
            thd_cmd = thd_cmd.encode("ascii")
            _online_port.write(thd_cmd)
            #generate_thd_sentence() ------  OR  ------------ _online_port.write(thd_cmd)
        
    #  distance from beth check not implemented    
    print("--------------Challenge 3 complete!-------------")
    return False

def logic_challege_3(_online_port, cmd, keep_loop_alive, logic_executed):
    if cmd.startswith("$GPRMC"):
        # rmc_cmd = [degrees, N/S, degrees, W/E, heading]
        rmc_cmd = get_location_coordinates(cmd)
        if not logic_executed:
            keep_loop_alive = rads_jebany_function(rmc_cmd)
            logic_executed = True
            

    # to send cmd to ship
    #  keep in mind to add * <checksum> to the command
    # _online_port.write(command)
    
    return keep_loop_alive, logic_executed


def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port(port)
    print("Setting up input console")

    keep_loop_alive = True
    logic_executed = False

    while keep_loop_alive:
        res = _online_port.readline().decode()
        print(res)
        try:
            keep_loop_alive, logic_executed = logic_challege_3(_online_port, res, keep_loop_alive, logic_executed)
        
        except Exception as e:
            print("Exception in logic ", e)



def start_program():
    list_of_ports = ports_module.check_ports()

    try:
        input_console_thread = threading.Thread(target=setup_input_console)
        listening_console_thread = threading.Thread()

        print("Choose mode:\n1. Input console\n2. Listening console")

        try:
            mode_choice = int(input())

        except:
            exit()

        if mode_choice == 1:
            input_console_thread.start()

        # Setup listening console from main1.py
        elif mode_choice == 2:
            listening_console_thread = threading.Thread(target=main1.setup_listening_console, args=(list_of_ports[1],))

        else:
            print(f"Option not available {mode_choice}")
            exit()

    except OSError as oe:
        print("There is a problem with configuring the port", oe)
  

if __name__ == "__main__":
    start_program(ports_module.connect_to_port("COM5"))
