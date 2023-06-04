# MAChallenge23
TeamSolent Autopilot project

## Challenge 1 prerequsites
1. OpenCPN set to 127.0.0.1 port 2947 protocol UDP
    a) Show NMEA Debug Window to check the connection
2. Make sure external coms are enabled
3. Start the script
    a) If it doesn't work insert $CCNVO,2,1.0,0,0*4A into input console

## Challenge 2 prerequsites
`Follow Challenge 1 above`

## Challenge 4 prerequsites
1. Open ShipSim3.
2. Load Plume onto the map (Do not forget to tick generate SIG commands).
3. Go to Comms and create a new NMEA interface.
4. Create TCP server on 127.0.0.1 port 49699
5. Enable ACK, MCO and RST flags in Receive tab.
6. In Transmit, enable RMC1 and SIG