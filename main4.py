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

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 49699

# TODO: create json with config for threshold of pollution
THRESHOLD = 12


# $CCTHD,85.00,0.00,0.00,0.00,0.00,85.00,0.00,0.00

def send_cmd_to_system(cmd):
    _online_port = ports_module.connect_to_port("COM5")
    _online_port.write(cmd)
    res = _online_port.readline().decode()
    print(res)

def write_to_log(sig_cmd, rmc_cmd):
    with open("./challenge4.log", "a+") as file:
        time = datetime.now()
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"{timestamp}: {rmc_cmd[0]}{rmc_cmd[1]}  {rmc_cmd[2]}{rmc_cmd[3]}  {sig_cmd}%"
        file.write(log_entry + "\n")

def get_pollution_level_from_DYSIG(cmd):
    # print(cmd.split(",")[1].split("*")[0])
    return cmd.split(",")[1].split("*")[0]


def get_location_coordinates(cmd):
    sentence = cmd.split(",")
    # [3] [4] [5] [6]
    return [sentence[3], sentence[4], sentence[5], sentence[6]]


def take_90_degrees_right_turn():
    # $CCHSC,210.00,T,210.00,M
    print("Taking turn right")
    hsc_sentence = generate_thd_hsc.generate_hsc_sentence(210.0)
    hsc_sentence = hsc_sentence + "*" + main1.calculate_checksum(hsc_sentence[1:])
    hsc_sentence = hsc_sentence + "\r\n"
    hsc_sentence = hsc_sentence.encode("ascii")
    send_cmd_to_system(hsc_sentence)

# This is where we do the Igor's algorithm, we have the info we need at the interval of 1 second

IS_IN_PLUME = False 
PLUME_ITER = 0
def algo_challenge4(sig_cmd, rmc_cmd):
    def set_true_in_plume():
        is_in_plume = True

    def set_false_in_plume():
        is_in_plume = False

    print(sig_cmd, rmc_cmd)
    if IS_IN_PLUME:
        if sig_cmd < THRESHOLD:
            print("Left Plume", rmc_cmd[0], rmc_cmd[1], rmc_cmd[2], rmc_cmd[3])
            IS_IN_PLUME = False
            if PLUME_ITER > 0:
                # Take a turn
                take_90_degrees_right_turn()
            PLUME_ITER += 1


    elif sig_cmd > THRESHOLD:
        print("Entered plume", rmc_cmd[0], rmc_cmd[1], rmc_cmd[2], rmc_cmd[3])
        is_in_plume = True


def start_search():
    # main1.send_cmd(cmd)
    # main1.calculate_checksum(sentence)
    # main1.check_obsticle_distance(cur_lat, cur_lon)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((SERVER_ADDR, SERVER_PORT))

    print("Starting the challenge")
    print("Setting forward thrust")
    
    # Turn on the boat
    turn_on_cmd = "$CCAPM,0,64,0,80"
    turn_on_cmd = turn_on_cmd + "*" + main1.calculate_checksum(turn_on_cmd[1:])
    turn_on_cmd = turn_on_cmd + "\r\n"
    turn_on_cmd = turn_on_cmd.encode("ascii")
    print(turn_on_cmd)
    send_cmd_to_system(turn_on_cmd)

    # Start moving forward 20% thrust
    fwd_sentence = generate_thd_hsc.generate_thd_sentence(20)
    fwd_sentence = fwd_sentence + "*" + main1.calculate_checksum(fwd_sentence[1:])
    fwd_sentence = fwd_sentence + "\r\n"
    fwd_sentence = fwd_sentence.encode("ascii")
    print(fwd_sentence)
    send_cmd_to_system(fwd_sentence)

    previous_cmd = ""

    while True:
        # Receive data from the server with buffer size
        tcp_data = sock.recv(1024)
        data_decoded = tcp_data.decode('utf-8')
        if data_decoded.startswith("$DYSIG"):
            pollution_level = get_pollution_level_from_DYSIG(data_decoded)
            rmc_coords = get_location_coordinates(previous_cmd)
            algo_challenge4(pollution_level, rmc_coords)
            write_to_log(pollution_level, rmc_coords)
        # get the most recent RMC command
        else:
            previous_cmd = data_decoded

    sock.close()


if __name__ == "__main__":
    start_search()