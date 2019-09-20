import math

R = 6371e3
M = 0.000621371

# Give four variables
# returns meters and miles
def LatLongToDistance(lat1, long1, lat2, long2):
    degreesToRadians = math.pi/180.0

    phi1 = (90.0 - lat1)*degreesToRadians
    phi2 = (90.0 - lat2)*degreesToRadians

    theta1 = long1*degreesToRadians
    theta2 = long2*degreesToRadians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
    math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    return [round(arc * R ), round(arc * R * M, 2 )]
