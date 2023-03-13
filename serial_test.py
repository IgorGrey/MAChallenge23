import serial # Define the USB ports

port1 = "COM5"
port2 = "COM6" # Define the baud rate

baud_rate = 115200 # Define the NMEA commands to send
# nmea_commands = ["$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68", "$GPGGA,225446,4916.45,N,12311.12,W,1,04,2.0,0012,M,-013,M,,*47"] # Open the serial ports

nmea_cmd = [
    "$CCAPM,0,64,0,80*56", 
    "$CCTHD,25.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00*6F",
    "$CCTHD,25.00,0.00,0.00,0.00,0.00,20.00,0.00,0.00*5D",
    "$CCAPM,7,64,0,80*51",
    "$CCHSC,45.0,T,,*13"
]


# serial_port1 = serial.Serial(port1, baud_rate)
serial_port2 = serial.Serial(port2, baud_rate) # Send NMEA commands via serial port 1

# serial_port1.write(nmea_cmd[2].encode())

# def send_command(cmd):
    # serial_port1.write(cmd.encode())
    # for i in serial_port2.readline():
    # print(serial_port2.read_all().decode())

while True:
    print(serial_port2.readline().decode())
    
    

response = serial_port2.readline()

print(response.decode().strip())

serial_port1.close()
serial_port2.close()
# for command in nmea_commands:
#     serial_port1.write(command.encode()) # Receive NMEA commands via serial port 2
# while True:
#     try:
#         message = serial_port2.readline().decode()
#         print(message)
#     except KeyboardInterrupt:
#         break # Close the serial ports
# serial_port1.close()
# serial_port2.close() 

# we first define the USB ports (port1 and port2) and the baud rate (baud_rate). We then define two NMEA commands (nmea_commands) that we want to send via serial port 1. We open the serial ports using the serial.Serial function and send the NMEA commands via serial port 1 using the serial_port1.write() function.We then receive NMEA commands via serial port 2 using a while loop that continuously reads the serial port using the serial_port2.readline() function. We print the received messages to the console. The while loop runs until we interrupt it with a keyboard interrupt (Ctrl+C).Finally, we close both serial ports using the serial_port.close() function. Note that you may need to modify the USB port names depending on your system configuration.

