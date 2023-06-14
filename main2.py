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

waypoints = [50.845, -0.746623, 50.845498, -0.746619,
             50.845496, -0.745935, 50.845006, -0.745927,
             50.845475, -0.745747, 50.845278, -0.745642,
             50.844937, -0.745483, 50.84491, -0.746166]
waypoints.reverse()

past_waypoints = []

obstacles = []


def chal2_logic(loop_keep_alive):
    pass


def get_ttm_smallest_distance(ttm_list):
    min_distance = float("inf")
    min_key = None

    for key, distance in ttm_list.items():
        current_distance = float(distance[1])
        if current_distance < min_distance:
            min_distance = current_distance
            min_key = key

    return min_key



def check_ttm_distance(ttm_cmd):
    ttm_one_line = ttm_cmd.split("\n")
    ttm_distances = {}
    for line in range(len(ttm_one_line)-1):
        ttm_split = ttm_one_line[line].split(",")
        ttm_distances[ttm_split[11]] = (ttm_split[11], ttm_split[2], ttm_split[3], ttm_split[14])
    
    dict_key = get_ttm_smallest_distance(ttm_distances)

    return ttm_distances[dict_key]
    

def get_tcp_data(sock_tcp):
    tcp_data = sock_tcp.recv(1024)
    return tcp_data.decode("utf-8")

latest_gprmc = None
gprmc_lock = threading.Lock()

def get_gprmc_data(_online_port):
    global latest_gprmc

    while True:
        gprmc_msg = _online_port.readline().decode()

        with gprmc_lock:
            latest_gprmc = gprmc_msg


def handle_both_challenges(_online_port):
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((config["general"]["server_addr"], config["chal2"]["server_tcp_port"]))

    rmc_thread = threading.Thread(target=get_gprmc_data, args=(_online_port,))
    rmc_thread.start()

    main1.start_sequence(_online_port)

    loop_keep_alive = True
    recovery_sequence = False
    rmc_msg = False
    set_start_speed = True
    rmc_msg = ""
    
    while loop_keep_alive:
        tcp_data = sock_tcp.recv(1024)
        ttm_decoded = tcp_data.decode("utf-8")

        with gprmc_lock:
            rmc_msg = latest_gprmc


        if ttm_decoded.startswith("$TTTTM") and rmc_msg:
            # TODO: check the distance for every object, if too close if statement execute
            object_close_prox = check_ttm_distance(ttm_decoded)
            # print("obj close prox", object_close_prox)
            if float(object_close_prox[1]) <= config["chal2"]["l0_obj_distance"]:
                print("Close proximity level 0")
                # Prepare to make a turn
                pass
                if float(object_close_prox[1]) <= config["chal2"]["l1_obj_distance"]:
                    print("Close proximity level 1")
                    # Make a turn
                    pass

            else:
                print("else statement", rmc_msg)
                if set_start_speed:
                    print("set speed")
                    thd_cmd = generate_thd_hsc.generate_thd_sentence(60)
                    thd_cmd = thd_cmd + "*" + main1.calculate_checksum(thd_cmd[1:])
                    thd_cmd = thd_cmd + "\r\n"
                    thd_cmd = thd_cmd.encode("ascii")
                    _online_port.write(thd_cmd)
                    set_start_speed = False
                loop_keep_alive, recovery_sequence = main1.handle_found_sentence(_online_port, 0, rmc_msg, waypoints, past_waypoints, loop_keep_alive, recovery_sequence)

        log_module.write_to_log_chal2_testing_ttm(ttm_decoded, "./chal2_ttm_test.log")

        # main 1
#  open=True>(port='COM5', baudrate=111520, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False) 0 $GPRMC,000022.48,A,5050.700364,N,00044.801892,W,2.6,276.0,230418,4.0,W,A,S*45
#  [-0.746166, 50.84491, -0.745483, 50.844937, -0.745642, 50.845278, -0.745747, 50.845475, -0.745927, 50.845006, -0.745935, 50.845496, -0.746619, 50.845498] [-0.746623, 50.845] True True

        # main 2
# open=True>(port='COM5', baudrate=111520, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False) 0 $GPRMC,000050.67,A,5050.724929,N,00044.798176,W,1.9,8.2,230418,4.0,W,A,S*41
#  [-0.746166, 50.84491, -0.745483, 50.844937, -0.745642, 50.845278, -0.745747, 50.845475, -0.745927, 50.845006, -0.745935, 50.845496, -0.746619, 50.845498, -0.746623, 50.845] [] True False

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