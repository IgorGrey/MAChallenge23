# Precondition:
    # List of hardcoded co-ords allocated precisely to match straight line for berthing to evoid early collision (lat, lon)
    # List berth_data = [] of hardcoded co-ords of existing berth locations [berth_name, berth(lat,lon), berth_starting_loc - lon), safe_approach_loc1(lat,lon), safe_approach_loc2(lat,lon), berth_starting_loc - lat, ]
                                                                            # UPDATED ORDER~
    # Speed control measures
#-----------------------REDUNDAND--------------
    # Maybe HEADING HOLD sentence figured out to help keeping steady heading
    # LIDAR used for keeping distance 1m away from berth (COMPLICATED LOGIC TO CONTROL BOAT WITH THD AND HSC)
    
    # go on goggle maps and retreave real:
        # co-ords for startring area loc's
        # co-ords for safe berth aproach loc's

    # get currrent boat's loc --- Stage 1: start
    # if not within safe_area (to work out that we add one or two wpns iside the area and check against them)
        # got to clothest safe area loc
        # confirm we are withing save area
    # check witch berth to go to (GIVEN) --- Stage 2: get to clothest beth safe location
    # head to chosen_berth [-0(berth_starting_loc)] WPN for that berth
    # follow berth_data list location until reach the wpnt3 reducing speed significantly by every next WPN in the list # Stage --- Approach the berth

# funcs reused:
#   calc_distance()
#   calc_heading()
#   convert dd to ddm()?
#     (slow down) = send_speed() - (N_poisition in lsit * 3) 
#   send_speed() 


# checking if boat within safe area (middle of the lake) to evoid sending it towards known obstacle
# looking for closest safe wpnt to set heading to
# Stage 1: start
middleWpntSafeArea = []
safeAreaWpnts = []
currentLoc = [float, float]
all_berth_data = []
berth_name_or_number = "" # GIVEN BY ORGANISIRES! !! !!! STRING !!! !!
chosen_berth = [] # [berth_name, save_wpnt, wpnt1, wpnt2, wpnt3, berthLoc]

closestSafeAreaWpnts = [] # [[meters, lat, lon]] 
for safeAreaWpnt in safeAreaWpnts:
    m = calc_distance(currentLoc, safeAreaWpnt) # or safeAreaWpnt[0],safeAreaWpnt[1]
    closestSafeAreaWpnts.append(m,safeAreaWpnt[0],safeAreaWpnt[1])
actuallyClosestSafeWpnt = min(closestSafeAreaWpnts)

closestMiddleSafeAreaWpnts = [] # [[meters, lat, lon]]
for wpnt in middleWpntSafeArea:
    m = calc_distance(currentLoc, wpnt) # or  wpnt[0], wpnt[1]
    closestMiddleSafeAreaWpnts.append(m, wpnt[0], wpnt[1])
actuallyMiddleClosestSafeWpnt = min(closestMiddleSafeAreaWpnts)

if x:=calc_distance(currentLoc,actuallyClosestSafeWpnt) < y:=calc_dinstance(currentLoc,actuallyMiddleClosestSafeWpnt):
    h = calc_heading(currentLoc, actuallyClosestSafeWpnt) # send HDG
    distance = int

    # repeats for every time var actuallyClosestSafeWpnt is updated and distance to it less then 5m
    i = 1 
    while i < 5:
        distance = calc_distance(currentLoc, actuallyClosestSafeWpnt)
        if distance < 5:
            # Stage 2: get to clothest beth safe location
            if chosen_berth == "":
                for berth in all_berth_data:
                    # search in all_berth_data[0] for string "berth 1-1"
                    berth = chosen_berth
            actuallyClosestSafeWpnt = chosen_berth[i] # [lat, lon]
            h = calc_heading(currentLoc, actuallyClosestSafeWpnt) # send boat to HDG towards updated actuallyClosestSafeWpnt
            # send_speed(-(i * 3))
            +i

# final heading and distance from beth checks?    
print("--------------Challenge 3 complete!-------------")

