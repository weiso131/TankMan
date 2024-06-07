from util import *
import random
def getMinDisOppo(data):
    selfX = data['x']
    selfY = data['y']
    competitorData = data['competitor_info']

    targetX = 1e4
    targetY = 1e4
    for c in competitorData:
        competitorX = c['x']
        competitorY = c['y']

        if (getDistance(targetX, targetY, selfX, selfY) > getDistance(competitorX, competitorY, selfX, selfY) and c['lives'] > 0):
            targetX = competitorX
            targetY = competitorY
    return targetX, targetY


def getTargetAngleGap(selfX, selfY, selfAngle, targetX, targetY, dis):
    target_vec_cos = getXVec(selfX, targetX) / dis
    target_vec_sin = getYVec(selfY, targetY) / dis

    targetAngle = (np.degrees(np.arctan2(target_vec_sin, target_vec_cos)) + 360) % 360

    return targetAngle - selfAngle
def Shoot(selfX, selfY, gunAngle, targetX, targetY, dis):
    angleGap = abs(getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis))
    angleTan = np.tan(angleGap / 180 * np.pi)

    if (angleGap <= 45 and dis * angleTan < 13 and dis < 300):
        return "SHOOT"
    return "NONE"
def TurnAngleToTarget(data):
    targetX, targetY = getMinDisOppo(data)
    selfX = data['x']
    selfY = data['y']
    gunAngle = (data['gun_angle'] + 540) % 360
    dis = getDistance(selfX, selfY, targetX, targetY)

    targetAngleGap = getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis)


    #檢查在這個炮口路徑上，子彈飛多遠會打到隊友
    teamMateShootDis = shootTeamMate(data, selfX, selfY, gunAngle)

    
    
    if (abs(targetAngleGap) <= 45):
        action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
        if (dis > teamMateShootDis or action == "NONE"):#dis > teamMateShoot代表會射到隊友
            return "NONE"
        return action
    
    elif (targetAngleGap > 0):
        return "AIM_LEFT"
    else:
        return "AIM_RIGHT"
    
def shootTeamMate(data, selfX, selfY, gunAngle):
    teamMateShoot = 1e4
    for tm in data['teammate_info']:
        if ((tm['x'] != selfX or tm['y'] != selfY) and tm['lives'] > 0):
            tmDis = getDistance(selfX, selfY, tm['x'], tm['y'])
            tmAngleGap = getTargetAngleGap(selfX, selfY, gunAngle, tm['x'], tm['y'], tmDis)
            if (abs(tmAngleGap) <= 45 and Shoot(selfX, selfY, gunAngle=gunAngle, targetX=tm['x'], targetY=tm['y'], dis=tmDis) == "SHOOT" and tmDis < teamMateShoot):
                teamMateShoot = tmDis  
    return teamMateShoot


def shootWall(graph, data):
    gunAngle = (data['gun_angle'] + 540) % 360
    angle = (data['angle'] + 540) % 360
    
    x, y = data['x'] + 5 * int(angle % 90 != 0) + 12.5, data['y'] + 5 * int(angle % 90 != 0) + 12.5 #方位補正，轉到斜的座標會-5
    graphX, graphY = int(x / 25), int(y / 25)
    
    

    for horizon_angle in range(0, 181, 180):
        teamMateShootDis = shootTeamMate(data, x, y, horizon_angle)
        wallThisAngle = haveWall(graph, graphX, graphY, horizon_angle)
        if (wallThisAngle != 1e4 and wallThisAngle < teamMateShootDis ):
            if (gunAngle == horizon_angle):
                return "SHOOT"
            elif (gunAngle > horizon_angle):
                return "AIM_RIGHT"
            else:
                return "AIM_LEFT"
        
    
    if (abs(x - 500) > 125):
        return "FORWARD"
    elif (angle != 90):
        if (angle > 90):
            return "TURN_RIGHT"
        else:
            return "TURN_LEFT"


    
    return random.choice(["FORWARD", "BACKWARD"])


def PosNag(num):
    if (abs(num) < 1e-9):
        return 0
    elif (num > 0):
        return 1
    elif (num < 0):
        return -1

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
    return 1e4


def enemy(graph, data):
    x, y = data['x'], data['y']
    