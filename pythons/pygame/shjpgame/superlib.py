import math
def Angle(x1, y1, x2, y2):       #### Angle from 2 points coordinates
    dx = x1 - x2
    dy = y1 - y2
    if dx == 0:
        if dy > 0:
            return 180
        elif dy < 0:
            return 0
        else:
            return None
    oa = float(dy)/float(dx)
    theta = math.degrees(math.atan(oa)) + 90.0
    if dx > 0:
        return theta
    else:
        return 180+theta
    return theta             ### return Angle, INT

def Distance(x1, y1, x2, y2):           ##### Distance from 2 points coordinates
    dist = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return dist                 ### return Distance, INT

def Move(x1, y1, angle, speed):         ##### Move 1 point from angle and speed
        gogo = math.sin(angle/180.*math.pi)
        gugu = math.cos(angle/180.*math.pi)
        x1 = x1 + speed*gogo
        y1 = y1 - speed*gugu
        return gogo, gugu             #### return Point, INT
