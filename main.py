import serial
import ports_module 
import subprocess
import threading


def setup_input_console(port="COM5"):
    _online_port = ports_module.connect_to_port(port)
    def handle_reponses():
        while True:
            res = _online_port.readline().decode()
            if res:
                print(res)
    
    response_thread = threading.Thread(target=handle_reponses)
    response_thread.start()

    while True:
        new_cmd = input("Enter a command:")
        if new_cmd:
            _online_port.write(new_cmd)
        

def setup_listening_console(port="COM6"):
    _online_port = ports_module.connect_to_port(port)
    while True:
        print(_online_port.readline().decode())


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