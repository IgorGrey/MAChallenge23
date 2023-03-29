import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 2947

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))

def send_cmd(cmd):
    new_cmd = f"{cmd}\r\n".encode("ascii")
    sock.sendto(new_cmd, (UDP_IP, UDP_PORT))

i = 20 
while True:
    # cmd = input()
    # cmd = cmd + "\r\n"
    time.sleep(5)
    cmd = f"$GPRMC,001115.81,A,{i}50.700849,N,00044.822914,W,0.0,269.7,230418,4.0,W,A*43\r\n"
    print("Sent", cmd)
    send_cmd(cmd)
    i += 1