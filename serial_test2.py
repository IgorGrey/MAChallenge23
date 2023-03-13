import serial # Define the USB ports

port1 = "COM5"
port2 = "COM6" # Define the baud rate

baud_rate = 115200 # Define the NMEA commands to send

nmea_cmd = [
    b"$CCAPM,0,64,0,80*56\n", 
    b"$CCTHD,25.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00*6F\n",
    b"$CCTHD,25.00,0.00,0.00,0.00,0.00,20.00,0.00,0.00*5D\n",
    b"$CCAPM,7,64,0,80*51\n",
    b"$CCHSC,45.0,T,,*13\n"
]

serial_port1 = serial.Serial(port1, baud_rate)

while True:
    new_cmd = int(input())
    if new_cmd == 5:
        cmd = input()
        serial_port1.write(b"$MMWPL,5050L710799,N,00044,755897,W,WPT 1")
    serial_port1.write(nmea_cmd[new_cmd])
    print(serial_port1.read_all().decode())