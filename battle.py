from util import *
from playerAlgorithm import goTarget
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

def TurnAngleToTarget(data):
    targetX, targetY = getMinDisOppo(data)
    selfX = data['x']
    selfY = data['y']
    selfAngle = (data['gun_angle'] + 540) % 360
    dis = getDistance(selfX, selfY, targetX, targetY)
    target_vec_cos = getXVec(selfX, targetX) / dis
    target_vec_sin = getYVec(selfY, targetY) / dis

    
    targetAngle = (np.degrees(np.arctan2(target_vec_sin, target_vec_cos)) + 360) % 360
    if (abs(selfAngle - targetAngle) <= 45):
        action = Shoot(dis, abs(selfAngle - targetAngle))
        if (action == "NONE"):
            action = goTarget(targetX, targetY, data)
        return action
    
    elif (targetAngle - selfAngle > 0):
        return "AIM_LEFT"
    else:
        return "AIM_RIGHT"
    
def Shoot(dis, angleGap):
    angleTan = np.tan(angleGap / 180 * np.pi)
    if (dis * angleTan < 10 and dis < 300):
        return "SHOOT"
    return "NONE"








