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

_LOG_FILE = "script_log.log"
_LOG_TIME_FORMAT = "%Y-%m-%D %H:%M:%S"

UDP_IP = "127.0.0.1"
UDP_PORT = 2947

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    # new_cmd = f"{cmd}\r\n".encode("ascii")
    # new_cmd = "$GPRMC,001115.81,A,5050.700849,N,00044.822914,W,0.0,269.7,230418,4.0,W,A,S*43"
    sock.sendto(cmd, (UDP_IP, UDP_PORT))


# LOGIC: [lat1, lon1, lat2, lon2,...]

heading_found = False

# waypoints = [ 50.845, 0.7459316167, 50.846, 0.7459316167, 
#               50.846, 0.7456465667,50.845, 0.7466465667,
#               50.845,0.7453615167,50.846,0.7453615167 ,
#               50.846,0.7450764667,50.845,0.7450764667 ]
# waypoints = [50.50710799, -000.44755897,50.50732397, -000.44755897,
#              50.50732394, -000.44738794, 50.50710799, -000.44798794,
#              50.50710799, -000.44721691, 50.50732397, -000.44721691,
#              50.50732397, -000.44704588, 50.50710799, -000.44704588]
# waypoints = [50.84517998333334 ,-0.7459316166666666,
#             50.84553995 ,-0.7459316166666666,
#             50.8455399 ,-0.7456465666666666,
#             50.84517998333334 ,-0.7466465666666667, 
#             50.84517998333334 ,-0.7453615166666666,
#             50.84553995 ,-0.7453615166666666,
#             50.84553995,-0.7450764666666667,
#             50.84517998333334 ,-0.7450764666666667]
            #try to reverse the list manually and get them by them one 
            # becuase it is 
waypoints = [50.845, -0.746623, 50.845498, -0.746619,
             50.845496, -0.745935, 50.845006, -0.745927,
             50.845475, -0.745747, 50.845278, -0.745642,
             50.844937, -0.745483, 50.84491 -0.746166 ]
waypoints.reverse()

# $CCAPM,7,64,0,80*51
# $CCTHD,85.00,0.00,0.00,0.00,0.00,85.00,0.00,0.00
# $CCAPT,2,5.0,K*3B
# $CCATC,17,1,1,50,0,2,0,20*65
# $MMWPL,5050.700022,N,00044.797410,W,WPT 1*07
# $MMWPL,5050.729901,N,00044.797159,W,WPT 2*0F
# $MMWPL,5050.729742,N,00044.756131,W,WPT 3*04
# $MMWPL,5050.700340,N,00044.755628,W,WPT 4*02
# $MMWPL,5050.728470,N,00044.744804,W,WPT 5*0D
# $MMWPL,5050.716710,N,00044.738512,W,WPT 6*07
# $MMWPL,5050.696208,N,00044.728947,W,WPT 7*0E
# $MMWPL,5050.694618,N,00044.769975,W,WPT 8*02
# $MMRTE,2,1,c,TRACK 1,WPT 1,WPT 2,WPT 3,WPT 4,WPT 5*13
# $MMRTE,2,2,c,TRACK 1,WPT 6,WPT 7,WPT 8*18
# $MMTKP,10,2,TRACK 1,TRACK 1,WPT 1,3.0,0.2,1000*3E
# $CCAPM,1,64,17,80*61


# TODO: Breakdown sentences, match them with patterns?

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



# Open powershell and run this script and listening port
# The same can be done for input if needed

"$CCTHD,25.00, 0.00,0.00,0.00,0.00,20.00,0.00,0.00"
"$CCTHD"


# IMPORTANT! Add which command you want to extract
input_list_of_cmds = {0: "GPRMC", 1: "THD..."}
listening_list_of_cmds = ["$GPRMC",]

# TODO: Commands of interest
# $GPRMC, 000305.39,   A,           5050.699892,N,          00044.772998,   W,         0.0,                0.0,                 230418,       4.0,  W  ,A   ,S   *41
# GPRMC, <Timestamp>, <GPS status>, <lat>, <lat_direction>, <long>, <long_direction>, <speed over ground>, <magnetic variation> <date_stamp>, <navigation status>
# GPRMC, <Timestamp>, <GPS status>, <lat>, <lat_direction>, <long>, <long_direction>, <speed over ground>, <track true> <date_stamp>, <mag variation> <mag dir> <mode ind>

# GPRMC what we need
# Time (UTC), status, lat, N/S, long, E/W, Speed over ground, track mode good, date (ddmmyy), magnetic variation deg, E/W, status (A/V)
# once without and once with converter


_online_port = ports_module.connect_to_port("COM5")
# IMPORTANT this is where the command of interest is passed to
def handle_found_sentence(sentence_num, nmea_sentence):
     if sentence_num == 0 :
# # ['$GPRMC', '000305.53', 'A', '5050.699892', 'N', '00044.772998', 'W', '0.0', '0.0', '230418', '4.0', 'W', 'A', 'S*4D']
        # gprmc_var = nmea_sentence.split(",")
        # timestamp = gprmc_var[1]
        # lat = float(gprmc_var[3])
        # lat = (lat/100)

        # latitude = latconverter.convert_minutes_to_degrees(lat)
        
        # lon = float(gprmc_var[5])
        # lon = (lon/100)
        
        # longitude = -(lonconverter.convert_minutes_to_degrees(lon))
    
        # heading_dir = gprmc_var[11]
        latitude,longitude = headingStandalone.extract_lat_lon(nmea_sentence)
        
        distance = distanceFormula.calculate_distance(latitude, longitude, waypoints [len(waypoints)-1], waypoints [len(waypoints)-2])
        print(distance)
        #print( latitude, longitude, waypoints [len(waypoints)-1], waypoints [len(waypoints)-2])
        #print(distance, "distance")

        if distance < 15:
            thd_sentence = generate_thd_hsc.generate_thd_sentence(17)
            thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
            thd_sentence = thd_sentence + "\r\n"
            thd_sentence = thd_sentence.encode("ascii")
            _online_port.write(thd_sentence)
            angle = angle_between_waypoints.angle_between_waypoints([(latitude, longitude), (waypoints[len(waypoints)-1], waypoints[len(waypoints)-2]), (waypoints[len(waypoints)-3], waypoints[len(waypoints)-4])])
            #print(heading_calc, "0")
            if angle <= 90: 
                thd_sentence = generate_thd_hsc.generate_hsc_sentence(1)
                thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                thd_sentence = thd_sentence + "\r\n"
                thd_sentence = thd_sentence.encode("ascii")
                _online_port.write(thd_sentence)
                if distance <= 15:
                    waypoints.pop()
                    waypoints.pop()
                    heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(heading_calc, "1")
                    print("Reached waypoint")
                    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                    hsc_sentence = hsc_sentence + "\r\n"
                    hsc_sentence = hsc_sentence.encode("ascii")
                    _online_port.write(hsc_sentence)
                    time.sleep(10)
                    thd_sentence = generate_thd_hsc.generate_thd_sentence(84)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)
            else:
                if distance < 10:
                    waypoints.pop()
                    waypoints.pop()
                    heading_calc = headingFormula.calculate_heading(longitude, latitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(heading_calc, "2")
                    print("Reached waypoint")
                    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                    hsc_sentence = hsc_sentence + "\r\n"
                    hsc_sentence = hsc_sentence.encode("ascii")
                    _online_port.write(hsc_sentence)
                    time.sleep(5)
                    thd_sentence = generate_thd_hsc.generate_thd_sentence(84)
                    thd_sentence = thd_sentence + "*" + calculate_checksum(thd_sentence[1:])
                    thd_sentence = thd_sentence + "\r\n"
                    thd_sentence = thd_sentence.encode("ascii")
                    _online_port.write(thd_sentence)


            # elif angle < 90:
            #     pass
            # elif angle < 45 and distance < 15:
            #     pass
            # elif angle < 45 and distance < 10:
            #     pass
            # elif angle < 30 and distance < 5:
            #     pass


        # TODO: if opencpn complains about the last char, split and send without it, keep in mind checksum
        # print("To be sent", nmea_sentence)
        # time.sleep(0.8)

        # index = ["$GPRMC", "var1", "var2", "var3"] MUST BE STRING
        # index = ",".join(index)
        # index = index + "*" + calculate_checksum(index)
        # index = f"{index}\r\n".encode("ascii")
        # _online_port.write(new_cmd)

        send_cmd(nmea_sentence.encode("ascii"))


def setup_input_console(port="COM5"):
    def handle_reponses():
        i = 1
        while True:
            res = _online_port.readline().decode()
            if res:
                if res.startswith("$" + "GPRMC") and i == 1:
                    # gprmc_var = res.split(",")
                    # lat = float(gprmc_var[3])
                    # lat = (lat/100)
                    # latitude = latconverter.convert_minutes_to_degrees(lat)
                    # lon = float(gprmc_var[5])
                    # lon= (lon/100)
                    # longitude = -(lonconverter.convert_minutes_to_degrees(lon))
                    latitude, longitude = headingStandalone.extract_lat_lon(res)
                    heading_calc = headingFormula.calculate_heading(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2])
                    print(heading_calc)
                    print(latitude, longitude, waypoints[len(waypoints)-1], waypoints[len(waypoints)-2], "im here")
                    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(heading_calc)
                    hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
                    hsc_sentence = hsc_sentence + "\r\n"
                    hsc_sentence = hsc_sentence.encode("ascii")
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
            checksum = calculate_checksum(new_cmd[1:])
            new_cmd = new_cmd + "*" +  checksum
            # new_cmd = new_cmd.encode("ascii")
            # new_cmd = f"{new_cmd}\r\n"
            new_cmd = f"{new_cmd}\r\n".encode("ascii")
            if new_cmd:
                _online_port.write(new_cmd)
                print("Sent", new_cmd)
                # send_cmd(new_cmd)
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