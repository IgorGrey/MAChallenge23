
 import serial # Define the USB ports
port1 = "/dev/ttyUSB0"
port2 = "/dev/ttyUSB1" # Define the baud rate
baud_rate = 4800 # Define the NMEA commands to send
nmea_commands = ["$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68", "$GPGGA,225446,4916.45,N,12311.12,W,1,04,2.0,0012,M,-013,M,,*47"] # Open the serial ports
serial_port1 = serial.Serial(port1, baud_rate)
serial_port2 = serial.Serial(port2, baud_rate) # Send NMEA commands via serial port 1
for command in nmea_commands:
    serial_port1.write(command.encode()) # Receive NMEA commands via serial port 2
while True:
    try:
        message = serial_port2.readline().decode()
        print(message)
    except KeyboardInterrupt:
        break # Close the serial ports
serial_port1.close()
serial_port2.close() 

//we first define the USB ports (port1 and port2) and the baud rate (baud_rate). We then define two NMEA commands (nmea_commands) that we want to send via serial port 1. We open the serial ports using the serial.Serial function and send the NMEA commands via serial port 1 using the serial_port1.write() function.We then receive NMEA commands via serial port 2 using a while loop that continuously reads the serial port using the serial_port2.readline() function. We print the received messages to the console. The while loop runs until we interrupt it with a keyboard interrupt (Ctrl+C).Finally, we close both serial ports using the serial_port.close() function. Note that you may need to modify the USB port names depending on your system configuration.

