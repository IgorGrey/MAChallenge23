# Precondition:
    # List of hardcoded co-ords allocated precisely to match straight line for berthing to evoid early collision (lat, lon)
    # List berth_data = [] of hardcoded co-ords of existing berth locations [berth1(lat,lon), safe_approach_loc1(lat,lon), safe_approach_loc2(lat,lon), berth_starting_loc(lat,lon)]
    # Speed control measures
#-----------------------REDUNDAND--------------
    # Maybe HEADING HOLD sentence figured out to help keeping steady heading
    # LIDAR used for keeping distance 1m away from berth (COMPLICATED LOGIC TO CONTROL BOAT WITH THD AND HSC)
    
    # go on goggle maps and retreave real:
        # co-ords for startring area loc's
        # co-ords for safe berth aproach loc's

    # get currrent boat's loc --- Stage 1: start
    # if not within safe_area 
        # got to clothest safe area loc
        # confirm we are withing save area
    # check witch berth to go to (GIVEN) --- Stage 2: get to clothest beth safe location
    # head to berth_data[-0(berth_starting_loc)] WPN for that berth
    # follow berth_data list location (backwards) until reach the berth reducing speed significantly by every next WPN in the list # Stage --- Approach the berth