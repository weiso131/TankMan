import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from usefulFunction import *

def ShootWall(gunAngle, wallLeft, wallRight, wallUp, wallDown):
    if (wallLeft == 1):
        return turnGunToWall(gunAngle, 180)
    if (wallRight == 1):
        return turnGunToWall(gunAngle, 0)
    if (wallUp == 1): 
        return turnGunToWall(gunAngle , 90)
    if (wallDown == 1):
        return turnGunToWall(gunAngle, 270)
    
    return "MEOW"

def turnGunToWall(gunAngle, wallAngle):
    if (gunAngle == wallAngle):
        return "SHOOT"
    elif (gunAngle > wallAngle):
        return "AIM_RIGHT"
    else:
        return "AIM_LEFT"
    
def haveWallFourWay(data, x, y, graph):
    """
    這個方向有沒有牆可以打
    wallRight, wallUp, wallLeft, wallDown
    """
    fourWay = []
    graphX, graphY = int(x / 25), int(y / 25)
    for horizon_angle in range(0, 360, 90):
        wallThisAngle = haveWall(graph, graphX, graphY, horizon_angle)
        if (wallThisAngle <= 300 and wallThisAngle < shootTeamMate(data, x, y, horizon_angle)):
            fourWay.append(1)
        else:
            fourWay.append(0)
    return tuple(fourWay)

def haveWall(graph, graphX, graphY, angle)->float:
    """
    return min dis of wall in this gun angle
    """
    cos, sin = PosNag(np.cos(angle / 180 * np.pi)), PosNag(np.sin(angle / 180 * np.pi))
    step = 8
    if (angle % 90 == 0):
        step = 12
    for i in range(step):
        if (graphY - sin * i < 0 or graphX + cos * i < 0 or graphY - sin * i >= 24 or graphX + cos * i >= 40):
            break
        if (int(graph[graphY - sin * i, graphX + cos * i]) > 0):
            return i * 25
    return 600