import serial
import ports_module 
import subprocess
import threading
import re
import nmea_cmds

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


def check_sentence(nmea_sentence):
    if not nmea_sentence.starts_with("$"):
        print("Missing $ sign")

    if not try_checksum(nmea_sentence):
        print("Checksum is not correct")

    # TODO: write commands that we need and requirements they must meet
    # {first NMEA chars: regex that needs to be met}
    pass

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