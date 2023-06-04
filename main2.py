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


with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd(cmd):
    sock.sendto(cmd, (config["general"]["server_addr"], config["general"]["opencpn_udp_port"]))

waypoints = []
waypoints.reverse()

obstacles = []

# calculate_checksum from main1.py

def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port("COM5")
    print("Setting up input console")

    def handle_responses():
        main1.start_sequence()

    try:
        response_thread = threading.Thread(target=handle_responses)
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
        input_console_thread = threading.Thread()
        listening_console_thread = threading.Thread()

        print("Choose mode:\n1. Input console\n2. Listening console")

        try:
            mode_choice = int(input())

        except:
            exit()

        if mode_choice == 1:
            input_console_thread.start(target=setup_input_console)

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