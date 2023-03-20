from serial.tools import list_ports
import serial


def check_ports(port0="COM5", port1="COM6", baud_rate=111520):
    print("Checking available ports...")
    all_ports = list_ports.comports()
    return_list = []

    for port in all_ports:
        print(f"Port: {port.device}")

        if port0 == str(port.device):
            print("Port1 found", port0)
            return_list.append(port0)

        elif port1 == str(port.device):
            print("Port2 found", port1)
            return_list.append(port1)

    if len(return_list) == 2:
        return return_list
    else:
        print("One of the ports is not available")
    
def connect_to_port(port, baudrate=111520):
    return serial.Serial(port, baudrate)


if __name__ == "__main__":
    check_ports()