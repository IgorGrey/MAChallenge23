import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 10110 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def send_cmd(cmd):
    new_cmd = f"{cmd}\r\n".encode("ascii")
    sock.sendto(new_cmd, (UDP_IP, UDP_PORT))


while True:
    # cmd = input()
    cmd = "$GPRMC,001115.81,A,5050.700849,N,00044.822914,W,0.0,269.7,230418,4.0,W,A,S*43"
    time.sleep(5)
    print("Sent", cmd)
    send_cmd(cmd)