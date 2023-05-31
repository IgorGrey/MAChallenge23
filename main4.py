import socket
import ports_module
import threading
import pynmea2
from datetime import datetime
import headingFormula
import generate_thd_hsc
import distanceFormula
import headingStandalone
import main1
import json

# TODO: create json with config for threshold of pollution, completed
# TODO: make sure the ship takes turn first, then makes decision
# This is to avoid the ship to start 150 degree turn to catch plume and 
# begin to catch plume again and start 30 degree turn
# TODO: when we enter plume, add some mechanism to prevent slightly lower value 
# to be registered in the next sentence activating next part of the code, completed

# $CCTHD,85.00,0.00,0.00,0.00,0.00,85.00,0.00,0.00

with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)


def send_cmd_to_system(cmd):
    _online_port = ports_module.connect_to_port("COM5")
    _online_port.write(cmd)
    res = _online_port.readline().decode()
    print(res)


def write_to_log(sig_cmd, rmc_cmd, fec_cmd):
    with open("./challenge4.log", "a+") as file:
        time = datetime.now()
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"{timestamp}: {rmc_cmd[0]}{rmc_cmd[1]}  {rmc_cmd[2]}{rmc_cmd[3]}  {sig_cmd}% Heading Direction {flags_list[2]}"
        file.write(log_entry + "\n")


def get_pollution_level_from_DYSIG(cmd):
    return cmd.split(",")[1].split("*")[0]


def get_location_coordinates(cmd):
    sentence = cmd.split(",")
    # return [sentence[3], sentence[4], sentence[5], sentence[6]]

    # Make sure the command is GPRMC
    if sentence[0] == "$GPRMC":
        if float(sentence[5]) < 00044.764329:
            take_90_degrees_right_turn(4)
        print(sentence[5])
        return [sentence[3], sentence[4], sentence[5], sentence[6]]
    else:
        return 0

    
def get_heading_degrees(cmd):
    sentence = cmd.split(",")
    return sentence[2]


def reset_heading():
    # $CCHSC,0,T,210.00,M
    print("Taking turn right")
    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(0)
    hsc_sentence = hsc_sentence + "*" + main1.calculate_checksum(hsc_sentence[1:])
    hsc_sentence = hsc_sentence + "\r\n"
    hsc_sentence = hsc_sentence.encode("ascii")
    send_cmd_to_system(hsc_sentence)


# Declare empty list
# After taking the first turn, save the coords into the list
# CASE 1: If plume not found, keep checking the distance with the last item in the list
#         If the distance met, start turning according to the rules
# CASE 2: If length of the list is 4, take a different turn, Left? if we took Right         
#         Clear the list
# CASE 3: If plume found, clean the list and continue


# TODO: remove
def take_90_degrees_right_turn(plume_iter):
    # $CCHSC,210.00,T,210.00,M
    print("Taking turn")
    if plume_iter == 0 or plume_iter == 1:
        turn_value = 90
    elif plume_iter == 4:
        turn_value = 180

    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(turn_value)
    hsc_sentence = hsc_sentence + "*" + main1.calculate_checksum(hsc_sentence[1:])
    hsc_sentence = hsc_sentence + "\r\n"
    hsc_sentence = hsc_sentence.encode("ascii")
    print(hsc_sentence)
    send_cmd_to_system(hsc_sentence)

# This is where we do the Igor's algorithm, we have the info we need at the interval of 1 second

def algo_challenge4(sig_cmd, rmc_cmd, is_in_plume, plume_iter, new_plume_sequence):
    # print(is_in_plume)
    # print(sig_cmd, rmc_cmd)

    # Leave plume sequence
    if is_in_plume and new_plume_sequence == 0:
        if float(sig_cmd) < config["chal4"]["threshold"]:
            is_in_plume = False

            # take_90_degrees_right_turn(plume_iter)
            plume_iter += 1

    # plume sequence jump prevention mechanism
    elif new_plume_sequence > 0:
        print("new plume sequence", new_plume_sequence)
        new_plume_sequence -= 1 

    # New plume found sequence
    elif float(sig_cmd) > config["chal4"]["threshold"]:
        print("Entered plume", rmc_cmd[0], rmc_cmd[1], rmc_cmd[2], rmc_cmd[3])
        is_in_plume = True
        new_plume_sequence = config["chal4"]["new_plume_sequence"]
    
    return is_in_plume, plume_iter, new_plume_sequence


flags_list = ["$DYSIG", "$GPRMC", "$CCFEC"]

def start_search():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((config["general"]["server_addr"], config["general"]["server_tcp_port"]))

    print("Starting the challenge")
    print("Setting forward thrust")
    
    # Turn on the boat
    turn_on_cmd = "$CCAPM,7,64,0,80"
    turn_on_cmd = turn_on_cmd + "*" + main1.calculate_checksum(turn_on_cmd[1:])
    turn_on_cmd = turn_on_cmd + "\r\n"
    turn_on_cmd = turn_on_cmd.encode("ascii")
    print(turn_on_cmd)
    send_cmd_to_system(turn_on_cmd)

    # Start moving forward 20% thrust
    fwd_sentence = generate_thd_hsc.generate_thd_sentence(config["chal4"]["plume_explore_speed"])
    fwd_sentence = fwd_sentence + "*" + main1.calculate_checksum(fwd_sentence[1:])
    fwd_sentence = fwd_sentence + "\r\n"
    fwd_sentence = fwd_sentence.encode("ascii")
    print(fwd_sentence)
    send_cmd_to_system(fwd_sentence)

    previous_cmd = ""
    heading_dir = ""
    rmc_coords = ""
    is_in_plume = False
    plume_iter = 0
    new_plume_sequence = 0

    # while True:
    #     # TODO: check if the logs update every second, possibly computer lagging?
    #     # If we need to use multithreading, check ChatGPT solution, should work for this project
    #     # reset_heading()
    #     # Receive data from the server with buffer size
    #     print("Connecting to TCP server")
    #     tcp_data = sock.recv(1024)
    #     data_decoded = tcp_data.decode('utf-8')
    #     print("Connected to the server")
    #     def first_solution():
    #         if data_decoded.startswith("$DYSIG"):
    #             pollution_level = get_pollution_level_from_DYSIG(data_decoded)
    #             rmc_coords = get_location_coordinates(previous_cmd)

    #             # Prevent incorrect DYSIG or GPRMC commands to get through
    #             if pollution_level and rmc_coords:
    #                 is_in_plume, plume_iter, new_plume_sequence = algo_challenge4(pollution_level, rmc_coords, is_in_plume, plume_iter, new_plume_sequence)
    #                 write_to_log(pollution_level, rmc_coords, heading_dir)

    #             else:
    #                 print("Caught incorrect DYSIG, GPRMC or CCFEC")
    #                 print(pollution_level, "\n", rmc_coords)

    #         # elif data_decoded.startswith("$GCHDM"):
    #         #     heading_dir = get_heading_degrees(data_decoded)

    #         # elif data_decoded.startswith("$GPRMC"):
    #         #     rmc_coords = get_location_coordinates(data_decoded)

    #         else:
    #             time = datetime.now()
    #             timestamp = time.strftime("%H:%M:%S")
    #             print(timestamp)
    #             previous_cmd = data_decoded

    def recieve_SIG_RMC_data():
        pollution_level = ""
        is_in_plume = False
        rmc_coords = ""
        heading_dir = 0
        plume_iter = ""
        new_plume_sequence = 0

        print("Connecting to the server")
        while True:
            tcp_data = sock.recv(1024)
            data_decoded = tcp_data.decode('utf-8')

            flag = data_decoded.split(",")[0]

            if flag == "$GPRMC":
                gprmc_coords = data_decoded
            
            elif flag == "$DYSIG":
                pollution_level = get_pollution_level_from_DYSIG(data_decoded)
                rmc_coords = get_location_coordinates(gprmc_coords)
                is_in_plume, plume_iter, new_plume_sequence = algo_challenge4(pollution_level, rmc_coords, is_in_plume, plume_iter, new_plume_sequence)
                write_to_log(pollution_level, rmc_coords, heading_dir)
            
            else:
                print("Caught incorrect DYSIG, GPRMC or CCFEC")
                print(pollution_level, "\n", rmc_coords)

    def recieve_heading_data():
        heading_dir = ""
        while True:
            tcp_data = sock.recv(1024)
            data_decoded = tcp_data.decode("utf-8")
            print(data_decoded)

            flag = data_decoded.split(",")[0]

            if flag == "$CCFEC":
                print("$CCFEC", flag)
                flags_list[2] = get_heading_degrees(data_decoded)
                # print(get_heading_degrees(data_decoded))
                print("FEC flag", flags_list[2])

    def multithread_solution():
        thread1 = threading.Thread(target=recieve_SIG_RMC_data)
        thread1.start()

        thread2 = threading.Thread(target=recieve_heading_data)
        # thread2.start()

        thread1.join()
        # thread2.join()

    multithread_solution()

    sock.close()


if __name__ == "__main__":
    start_search()