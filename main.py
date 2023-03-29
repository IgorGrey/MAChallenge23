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

_LOG_FILE = "script_log.log"
_LOG_TIME_FORMAT = "%Y-%m-%D %H:%M:%S"

UDP_IP = "127.0.0.1"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    new_cmd = f"{cmd}\r\n".encode("ascii")
    sock.sendto(new_cmd, (UDP_IP, UDP_PORT))


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
        
    return print(f"{checksum:02X}")

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

# IMPORTANT this is where the command of interest is passed to
def handle_found_sentence(sentence_num, nmea_sentence):

    if sentence_num == 0:
# ['$GPRMC', '000305.53', 'A', '5050.699892', 'N', '00044.772998', 'W', '0.0', '0.0', '230418', '4.0', 'W', 'A', 'S*4D']
        # gprmc_var = nmea_sentence[0].split(",")

        # TODO: if opencpn complains about the last char, split and send without it, keep in mind checksum
        send_cmd(nmea_sentence)


def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port(port)


    def handle_reponses():
        while True:
            res = _online_port.readline().decode()
            if res:
                for key, value in input_list_of_cmds.items():
                    if res.startswith("$" + value):
                        handle_found_sentence(key, res)
                # if res in input_list_of_cmds:
                #     print(res, "Found in a list <<<<")
                print(res)
    
    try:
        # response_thread = threading.Thread(target=handle_reponses)
        # response_thread.start()
        handle_reponses()

    except:
        pass
        # logger.error()

    while True:
        try:
            # INPUT FORMAT $COMMAND<NUMBERS>,<NUMBERS>,..<CHECKSUM>
            # OR SIMPLE WAY $SENTENCE*CHECKSUM
            new_cmd = input("Enter a command:")
            new_cmd = f"{new_cmd}\r\n".encode("ascii")
            if new_cmd:
                _online_port.write(new_cmd)
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