from geographiclib.geodesic import Geodesic
# Maybe lat and lon are the other way around
def generateOffset(lat1, lon1, shift, heading):
    geod = Geodesic.WGS84
    # What's the count for ??????????????????????????????????????????
    count = 0
    waypoints = []
    print(f"""Obstacle at: Lat: {lat1}\nLong {lon1}\nGenerating New Waypoints with an offset of {shift}\n
          Approaching at a heading of {heading}""") 
    # Needs explanation on funcionality of the loop
    for azi in [180, 225, 270, 315, 0]:
        newHeading = heading - azi
        if newHeading >= 360:
            newHeading = newHeading - 360
        elif newHeading < 0:
            newHeading = 360 + newHeading
        # What's the count for
        count += 1
        newWaypoint = geod.Direct(lat1, lon1, newHeading, shift)

        newLat = newWaypoint["lat2"]
        newLon = newWaypoint["lon2"]

        print(f"Lat: {newLat}\nLon: {newLon}\nHeading: {newHeading}\n Count: {count}")

        waypoints.append([newLat, newLon])

        return waypoints


if __name__ == "__main__":
    lat1 = 50.8449
    lon1 = -0.74621

generateOffset(50.8449, -0.74621, 20,350)