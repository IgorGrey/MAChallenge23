import socket
import ports_module
import threading
import pynmea2
import headingFormula
import generate_thd_hsc
import distanceFormula
import headingStandalone
import json
import main1
import log_module

with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    sock.sendto(cmd, (config["general"]["server_addr"], config["general"]["opencpn_udp_port"]))

waypoints = []
waypoints.reverse()

obstacles = []


def chal2_logic(loop_keep_alive):
    pass


def handle_both_challenges(_online_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config["general"]["server_addr"], config["chal2"]["server_tcp_port"]))
    
    while True:
        tcp_data = sock.recv(1024)
        ttm_decoded = tcp_data.decode("utf-8")
        # RMC_port = ports_module.connect_to_port("COM5")
        log_module.write_to_log_chal2_testing_ttm(ttm_decoded, "./chal2_ttm_test.log")

    # TTM_port = TCP server connect to get TTM commands
    
    # 1. If TTM received and it doesnt see any obstacles in the X range, proceed to continue with challenge 1
    # 2. 
    # main1.handle_responses(_online_port)


def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port("COM5")
    print("Setting up input console")

    try:
        response_thread = threading.Thread(target=handle_both_challenges, args=[_online_port])
        response_thread.start()
    
    except Exception as e:
        print("Handle_responses error: \n", e)

    while True:
        try:
            new_cmd = input("Enter a command:")
            checksum = main1.calculate_checksum(new_cmd[1:])
            new_cmd = new_cmd + "*" +  checksum
            new_cmd = f"{new_cmd}\r\n".encode("ascii")
            if new_cmd:
                _online_port.write(new_cmd)
                print("Sent", new_cmd)
        except:
            print("Error has occured")
            continue


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
        # There are no differences in code
        elif mode_choice == 2:
            listening_console_thread = threading.Thread(target=main1.setup_listening_console, args=(list_of_ports[1],))

        else:
            print(f"Option not available {mode_choice}")
            exit()

    except OSError as oe:
        print("There is a problem with configuring the port", oe)


if __name__ == "__main__":
    start_program()