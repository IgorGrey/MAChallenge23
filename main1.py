# import serial
import socket
import ports_module 
# import subprocess
import threading
# import re
# import logging
# import nmea_cmds
import pynmea2
from datetime import datetime
# import time
import headingFormula
import generate_thd_hsc
import angle_between_waypoints
# import calculateSpeed
import distanceFormula
# import lonconverter
# import latconverter
import headingStandalone
import json

# import pyais automatic identification system 
# json config file
with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    sock.sendto(cmd, (config["general"]["server_addr"], config["general"]["opencpn_udp_port"]))


heading_found = False
waypoints = [50.845, -0.746623, 50.845498, -0.746619,
             50.845496, -0.745935, 50.845006, -0.745927,
             50.845475, -0.745747, 50.845278, -0.745642,
             50.844937, -0.745483, 50.84491, -0.746166 ]
waypoints.reverse()

past_waypoints = []

obsticles = []

def calculate_checksum(sentence):
    checksum = 0

    for byte in sentence:
        checksum ^= ord(byte)
        
    return f"{checksum:02X}"

def try_checksum(checksum):
    sentence = checksum.split("*")

    print("Sentence", sentence)
    calculated_checksum = calculate_checksum(sentence[0][1:])

    if calculated_checksum == sentence[2]:
        print("Sentence", sentence, "is correct")
    else:
        print("Incorrect checksum")


def check_output_sentence(nmea_sentence):
    if not nmea_sentence.starts_with("$"):
        print("Missing $ sign")

    if not try_checksum(nmea_sentence):
        print("Checksum is not correct")


def check_input_sentence(nmea_sentence):
    if not nmea_sentence.starts_with("$"):
        nmea_sentence = "$" + nmea_sentence

    return nmea_sentence

def check_obsticle_distance(cur_lat, cur_lon):
    # for loc in range(len(obsticles), 2):
    #     ship_obj_distance = distanceFormula.calculate_distance(cur_lat, cur_lon, obsticles[loc], obsticles[loc+1])

    #     if ship_obj_distance < 20:
    #         return True

    return False


# IMPORTANT! Add which command you want to extract
input_list_of_cmds = {0: "GPRMC", 1: "THD...", 2: "OBST", 3: "BRTH", 4: "POLL", 5: "OBJT"}
listening_list_of_cmds = ["$GPRMC",]

def start_sequence(_online_port):
    cmd_1 = "$CCNVO,2,1.0,0,0*4A"
    cmd_1 = cmd_1 + "*" + calculate_checksum(cmd_1[1:])
    cmd_1 = cmd_1 + "\r\n"
    cmd_1 = cmd_1.encode("ascii")
    _online_port.write(cmd_1)
    
    cmd_2 = "$CCAPM,0,64,0,80"
    cmd_2 = cmd_2 + "*" + calculate_checksum(cmd_2[1:])
    cmd_2 = cmd_2 + "\r\n"
    cmd_2 = cmd_2.encode("ascii")
    _online_port.write(cmd_2)
    
    cmd_3 = "$CCAPM,7,64,0,80"
    cmd_3 = cmd_3 + "*" + calculate_checksum(cmd_3[1:])
    cmd_3 = cmd_3 + "\r\n"
    cmd_3 = cmd_3.encode("ascii")
    _online_port.write(cmd_3)

def swap_last_waypoints(past_waypoints):
    print(past_waypoints)
    past_waypoints[-1], past_waypoints[-2] = past_waypoints[-2], past_waypoints[-1] 
    print(past_waypoints)


def heading_notice_distance(_online_port, speed):
    thd_sentence = generate_thd_hsc.generate_thd_sentence(speed)
    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
    thd_sentence = thd_sentence + "\r\n"
    thd_sentence = thd_sentence.encode("ascii")
    _online_port.write(thd_sentence)


def heading_slowdown_distance(_online_port, lat, lon, waypoints):
    heading_calc = headingFormula.calculate_heading(lat, lon, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
    hsc_sentence = hsc_sentence + "\r\n"
    hsc_sentence = hsc_sentence.encode("ascii")
    _online_port.write(hsc_sentence)


def l3_distance(_online_port, lat, lon, waypoints, past_waypoints, speed):
    past_waypoints.append(waypoints.pop())
    past_waypoints.append(waypoints.pop())
    swap_last_waypoints(past_waypoints)
    heading_calc = headingFormula.calculate_heading(lat, lon, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
    print("-----------------------------")
    print("Current waypoint reached")
    print("Heading to the next Waypoint")
    print("-----------------------------")
    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
    hsc_sentence = hsc_sentence + "\r\n"
    hsc_sentence = hsc_sentence.encode("ascii")

    _online_port.write(hsc_sentence)
    thd_sentence = generate_thd_hsc.generate_thd_sentence(speed)
    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
    thd_sentence = thd_sentence + "\r\n"
    thd_sentence = thd_sentence.encode("ascii")
    _online_port.write(thd_sentence)

    return waypoints, past_waypoints


# IMPORTANT this is where the command of interest is passed to
def handle_found_sentence(_online_port, sentence_num, nmea_sentence, waypoints, past_waypoints, recovery_sequence):
    # if it is $GPRMC
    if sentence_num == 0:
        lat, lon = headingStandalone.extract_lat_lon(nmea_sentence)
        distance = distanceFormula.calculate_distance(lat, lon, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
        heading_calc = headingFormula.calculate_heading(lat, lon, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])        
        hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
        hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
        hsc_sentence = hsc_sentence + "\r\n"
        hsc_sentence = hsc_sentence.encode("ascii")
        _online_port.write(hsc_sentence)
        print("The heading is:", round(heading_calc, 0), " Distance to the next waypoint:",distance,"meters.")

        # The current waypoint is in notice distance
        if distance <= config["chal1"]["l1_distance"] and len(waypoints) != 0:
            heading_notice_distance(_online_port, config["chal1"]["l1_speed"])

            # The current waypoint is in slowdown distance
            if distance <= config["chal1"]["l2_distance"]:
                heading_slowdown_distance(_online_port, lat, lon, waypoints)
                
                # The current waypoint is reached
                if distance <= config["chal1"]["l3_distance"]:
                    waypoints, past_waypoints = l3_distance(_online_port, lat, lon, waypoints, past_waypoints, config["chal1"]["l3_speed"])
                    recovery_sequence = True

            # When the boat approaching the last waypoint
            elif distance <= config["chal1"]["l2_distance"] and len(waypoints) == 2:
                heading_slowdown_distance(_online_port, lat, lon, waypoints)

                if distance <= config["chal1"]["l3_distance"]:
                    # TODO: replace l3_distance with a new function
                    # l3_last_distance should not pop waypoints since they are no more of them
                    # could also be integrated into exisitng function and checked against the 
                    # length of the list
                    waypoints, past_waypoints = l3_distance(_online_port, lat, lon, waypoints, past_waypoints, config["chal1"]["last_l3_speed"])
        
        elif len(waypoints) == 0:
            print("-----------------------------")
            print("The last waypoint has been reached")
            print("-----------------------------")
            exit()

        elif recovery_sequence:
            recovery_distance = distanceFormula.calculate_distance(lat, lon, past_waypoints[-1], past_waypoints[-2])
            if recovery_distance >= 5:
                forward_thrust = generate_thd_hsc.generate_thd_sentence(config["chal1"]["l0_speed"])
                forward_thrust = forward_thrust + "*" + calculate_checksum(forward_thrust[1:])
                forward_thrust = forward_thrust + "\r\n"
                forward_thrust = forward_thrust.encode("ascii")
                _online_port.write(forward_thrust)
                recovery_sequence = False
                print(forward_thrust)

        # Create new function for rmc to opencpn
        send_cmd(nmea_sentence.encode("ascii"))

        print(recovery_sequence)
        return recovery_sequence


def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port("COM5")
    print("Setting up input console")
    def handle_reponses():
        print("Starting the serial port")
        i = 1

        # Sequences that allow to communicate with SPECTER aka Initialisation
        start_sequence(_online_port)

        # Recovery sequence during the turn, limits speed on turns
        recovery_sequence = False

        while True:
            res = _online_port.readline().decode()
            if res:
                if res.startswith("$" + "GPRMC") and i == 1:
                    # Created to reverse because the setup is for the shipSim should be changed!!!!!!!!!!!!

                    thd_sentence = generate_thd_hsc.generate_thd_sentence(-17)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)
                    print(thd_sentence)
                    print("speed set to 8% <=")
                
                    latitude, longitude = headingStandalone.extract_lat_lon(res)
                    heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(" New heading set to ===>")
                    print(heading_calc)
                    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                    hsc_sentence = hsc_sentence + "\r\n"
                    hsc_sentence = hsc_sentence.encode("ascii")

                    thd_sentence = generate_thd_hsc.generate_thd_sentence(17)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)

                    print(hsc_sentence)
                    _online_port.write(hsc_sentence)
                    print("Init")
                    i = 0

            # TODO: decide which flags we need, if only $GPRMC then remote for loop
            for key, value in input_list_of_cmds.items():
                    if res.startswith("$" + value):
                        recovery_sequence = handle_found_sentence(_online_port, key, res, waypoints, past_waypoints, recovery_sequence)
           
    try:
        response_thread = threading.Thread(target=handle_reponses)
        response_thread.start()

    except Exception as e:
        print("Line 206 listening error:", e)
        pass


    while True:
        try:
            new_cmd = input("Enter a command:")
            if new_cmd[:4] == input_list_of_cmds[2] or new_cmd[:4] == input_list_of_cmds[3] or new_cmd[:4] == input_list_of_cmds[4] or new_cmd[:4] == input_list_of_cmds[5]:
                pass
            else:
                checksum = calculate_checksum(new_cmd[1:])
                new_cmd = new_cmd + "*" +  checksum
                new_cmd = f"{new_cmd}\r\n".encode("ascii")
                if new_cmd:
                    _online_port.write(new_cmd)
                    print("Sent", new_cmd)
        except:
            print("Error has occured")
            continue
        
def setup_listening_console(port="COM6", baudrate=115200):
    _online_port = ports_module.connect_to_port(port)
    while True:
        response = _online_port.readline().decode()
        print(response)
        try:
            nmea_res = pynmea2.parse(response)
        except pynmea2.ParseError as pynmea_res:
            continue
    
        if nmea_res.sentence_type == "RMC":
            tkp = nmea_res.talker_id, nmea_res.datestamp, nmea_res.latitude, nmea_res.longitude

            print(tkp)


def start_program():
    list_of_ports = ports_module.check_ports()

    try:
        input_console_thread = threading.Thread(target=setup_input_console, args=(list_of_ports[0],))
        listening_console_thread = threading.Thread(target=setup_listening_console, args=(list_of_ports[1],))

        print("Choose mode:\n1. Input console\n2. Listening console")
        try:
            mode_choice = int(input())
        except:
            exit()

        if mode_choice == 1:
            input_console_thread.start()
        elif mode_choice == 2:
            listening_console_thread.start()
        else:
            print(f"Option not available {mode_choice}")
            exit()
    

    except OSError as oe:
        print("There is a problem with configuring the port", oe)
    


if __name__ == "__main__":
    start_program()