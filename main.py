import serial
import ports_module 
import subprocess
import threading
import pynmea2

# Open powershell and run this script and listening port
# The same can be done for input if needed

"$CCTHD,25.00, 0.00,0.00,0.00,0.00,20.00,0.00,0.00"
"$CCTHD"

input_list_of_cmds = []
listening_list_of_cmds = ["$GPRMC",]

def input_cmd_of_interest(cmd):
    pass

def listening_cmd_of_interest(cmd):
    pass

def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port(port)
    def handle_reponses():
        while True:
            res = _online_port.readline().decode()
            if res:
                if res in input_list_of_cmds:
                    input_cmd_of_interest(res)
                print(res)
    
    response_thread = threading.Thread(target=handle_reponses)
    response_thread.start()

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
        

def setup_listening_console(port="COM6", baudrate=9600):
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
    

    # TODO: setup 2 consoles, one listen to output from COM6
    # the second one connected to a COM5 which pushes responses
    # this is not the best implementation
    # cmd = f"powershell.exe -NoExit python .\main.py ''"
    # process1 = subprocess.Popen(['powershell.exe', '-Command', 'while ($true) { Receive-Output1 }'])
    # input_terminal = subprocess.Popen(["powershell", "-Command", "py -c 'from threading import Thread; from script import "])


if __name__ == "__main__":
    start_program()