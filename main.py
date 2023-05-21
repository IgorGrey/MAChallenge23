import serial
import socket
import ports_module 
import subprocess
import threading
import re
import logging
# import nmea_cmds
import pynmea2
from datetime import datetime
import time
import headingFormula
import generate_thd_hsc
import angle_between_waypoints
import calculateSpeed
import distanceFormula
import lonconverter
import latconverter
import headingStandalone
import object_avoidance

# import pyais automatic identification system 
# json config file

UDP_IP = "127.0.0.1"
UDP_PORT = 2947

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    # new_cmd = f"{cmd}\r\n".encode("ascii")
    # new_cmd = "$GPRMC,001115.81,A,5050.700849,N,00044.822914,W,0.0,269.7,230418,4.0,W,A,S*43"
    sock.sendto(cmd, (UDP_IP, UDP_PORT))


# LOGIC: [lat1, lon1, lat2, lon2,...]

heading_found = False
waypoints = [50.845, -0.746623, 50.845498, -0.746619,
             50.845496, -0.745935, 50.845006, -0.745927,
             50.845475, -0.745747, 50.845278, -0.745642,
             50.844937, -0.745483, 50.84491, -0.746166 ]
waypoints.reverse()

# Logic: [lat1, lon1, lat2, lon2]
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

    # TODO: write commands that we need and requirements they must meet
    # {first NMEA chars: regex that needs to be met}


def check_input_sentence(nmea_sentence):
    # Run checks if the sentence meets the basic rules
    # TODO: check if checksum is correct
    if not nmea_sentence.starts_with("$"):
        nmea_sentence = "$" + nmea_sentence

    return nmea_sentence

def check_obsticle_distance(cur_lat, cur_lon):
    for loc in range(len(obsticles), 2):
        ship_obj_distance = distanceFormula.calculate_distance(cur_lat, cur_lon, obsticles[loc], obsticles[loc+1])

        if ship_obj_distance < 20:
            return True

    return False


# IMPORTANT! Add which command you want to extract
input_list_of_cmds = {0: "GPRMC", 1: "THD...", 2: "OBST", 3: "BRTH", 4: "POLL", 5: "OBJT"}
listening_list_of_cmds = ["$GPRMC",]

# IMPORTANT this is where the command of interest is passed to

current_mode = 0

def handle_found_sentence(sentence_num, nmea_sentence):
    _online_port = ports_module.connect_to_port("COM5")
    if sentence_num == 0 and current_mode == 0:

        latitude, longitude = headingStandalone.extract_lat_lon(nmea_sentence)
        
        distance = distanceFormula.calculate_distance(latitude, longitude, waypoints [len(waypoints)-1], waypoints [len(waypoints)-2])
        
        heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])        
        hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
        hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
        hsc_sentence = hsc_sentence + "\r\n"
        hsc_sentence = hsc_sentence.encode("ascii")
        print("The heading is:", round(heading_calc, 0), " Distance to the next waypoint:",distance,"meters.")
        _online_port.write(hsc_sentence)

        # TODO, ensure that this function is triggered once until the waypoint is complited
        if check_obsticle_distance(latitude, longitude):
            pass

        #  Check all obsticles and calculate their distances DONE
        # if Obsticle in range of 20 meters away trigger function DONE
        # Calculate the angle that is safe to avoid the obsticle
        # put waypoint in the distance 20 minutes away with the previously calculated angle
        # add the waypoint as the first (current) point to head to
        new_lat, new_lon = 0, 0
        waypoints.append(new_lat, new_lon)

        if distance <= 15:
            thd_sentence = generate_thd_hsc.generate_thd_sentence(17)
            thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
            thd_sentence = thd_sentence + "\r\n"
            thd_sentence = thd_sentence.encode("ascii")
            _online_port.write(thd_sentence)

            if distance <= 7:
                
                heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                # print(heading_calc, "Heading set to <==")
                
                hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                hsc_sentence = hsc_sentence + "\r\n"
                hsc_sentence = hsc_sentence.encode("ascii")
                _online_port.write(hsc_sentence)
                
                if distance <= 3:
                    waypoints.pop()
                    waypoints.pop()
                    heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(heading_calc, "Heading set to <==")
                    print("Reached waypoint")
                    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                    hsc_sentence = hsc_sentence + "\r\n"
                    hsc_sentence = hsc_sentence.encode("ascii")
                    _online_port.write(hsc_sentence)
                    thd_sentence = generate_thd_hsc.generate_thd_sentence(17)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)

        # Create new function for rmc to opencpn
        send_cmd(nmea_sentence.encode("ascii"))

    elif current_mode == 4:
        print("Mode 4 on")

def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port("COM5")
    def handle_reponses():
        i = 1
        while True:
            res = _online_port.readline().decode()
            if res:
                if res.startswith("$" + "GPRMC") and i == 1:
                    thd_sentence = generate_thd_hsc.generate_thd_sentence(-17)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)
                    print("speed set to 8% <=")

                    latitude, longitude = headingStandalone.extract_lat_lon(res)
                    heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(" New heading set to ===>")
                    print(heading_calc)
                    # print(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2], "im here")
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


            for key, value in input_list_of_cmds.items():
                    if res.startswith("$" + value):
                        handle_found_sentence(key, res)
           
                # if res in input_list_of_cmds:
                #     print(res, "Found in a list <<<<")
                # print(res)
    
    try:
        response_thread = threading.Thread(target=handle_reponses)
        response_thread.start()
        # handle_reponses()

    except:
        pass
        # logger.error()

    while True:
        try:
            # INPUT FORMAT $COMMAND<NUMBERS>,<NUMBERS>,..<CHECKSUM>
            # OR SIMPLE WAY $SENTENCE*CHECKSUM
            new_cmd = input("Enter a command:")
            if new_cmd[:4] == input_list_of_cmds[2] or new_cmd[:4] == input_list_of_cmds[3] or new_cmd[:4] == input_list_of_cmds[4] or new_cmd[:4] == input_list_of_cmds[5]:
                pass
            elif new_cmd == "Mode4":
                current_mode = 4
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
        mode_choice = int(input())

        if mode_choice == 1:
            input_console_thread.start()
        elif mode_choice == 2:
            listening_console_thread.start()
        else:
            print(f"Option not available {mode_choice}")
    

    except OSError as oe:
        print("There is a problem with configuring the port", oe)
    


if __name__ == "__main__":
    # Start logger
    # logger = logging.getLogger(__name__)
    # file_handler = logging.FileHandler(_LOG_FILE)
    # log_formatter = logging.Formatter("{asctime}: {level} {message}")
    # formatter = logging.Formatter(log_formatter, style="{")
    # file_handler.setFormatter(log_formatter)
    # logger.addHandler(file_handler)
    # logger.info("Script has started")

    start_program()