import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from usefulFunction import *



def turnGunToWall(gunAngle, wallAngle):
    if (gunAngle == wallAngle):
        return "SHOOT"
    elif (gunAngle > wallAngle):
        return "AIM_RIGHT"
    else:
        return "AIM_LEFT"
    
def getShootWallAgree(x, y, wallAngle, data, graph):
    """
    確保不會打到人
    """
    tmDis = shootTeamMate(data, x, y, wallAngle)

    if (haveWall(graph, int(x / 25), int(y / 25), wallAngle) < min(300, tmDis)):
        return True
    
    return False

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