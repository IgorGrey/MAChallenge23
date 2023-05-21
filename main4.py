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


# $CCTHD,85.00,0.00,0.00,0.00,0.00,85.00,0.00,0.00

def send_cmd_to_system(cmd):
    _online_port = ports_module.connect_to_port("COM5")
    _online_port.write(cmd)

def write_to_log(cmd):
    with open("./challenge4.log", "a+") as file:
        time = datetime.now()
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"{timestamp}: {cmd}"
        file.write(log_entry + "\n")

def get_pollution_level_from_DYSIG(cmd):
    # print(cmd.split(",")[1].split("*")[0])
    return cmd.split(",")[1].split("*")[0]


def start_search():
    # main1.send_cmd(cmd)
    # main1.calculate_checksum(sentence)
    # main1.check_obsticle_distance(cur_lat, cur_lon)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((SERVER_ADDR, SERVER_PORT))

    print("Starting the challenge")
    print("Setting forward thrust")
    
    turn_on_cmd = "$CCAPM,0,64,0,80"
    turn_on_cmd = turn_on_cmd + "*" + main1.calculate_checksum(turn_on_cmd[1:])
    turn_on_cmd = turn_on_cmd + "\r\n"
    turn_on_cmd = turn_on_cmd.encode("ascii")
    send_cmd_to_system(turn_on_cmd)

    fwd_sentence = generate_thd_hsc.generate_thd_sentence(20)
    fwd_sentence = fwd_sentence + "*" + main1.calculate_checksum(fwd_sentence[1:])
    fwd_sentence = fwd_sentence + "\r\n"
    fwd_sentence = fwd_sentence.encode("ascii")
    print(fwd_sentence)
    send_cmd_to_system(fwd_sentence)

    # hsc_sentence = hsc_sentence + "*" + calculate_checksum(hsc_sentence[1:])
    # hsc_sentence = hsc_sentence + "\r\n"
    # hsc_sentence = hsc_sentence.encode("ascii")

    while True:
        # Receive data from the server with buffer size
        tcp_data = sock.recv(1024)
        data_decoded = tcp_data.decode('utf-8')
        pollution_level = get_pollution_level_from_DYSIG(data_decoded)
        write_to_log(pollution_level)

    sock.close()



if __name__ == "__main__":
    start_search()