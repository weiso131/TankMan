from battle import *
from util import *

def testDataForAgent(dataForAgent):
    x, y, Angle, gunAngle, hitTmDis, wallUp, wallDown, wallLeft, wallRight,\
    e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(dataForAgent)
    
    enemyFind = []

    if (enemyShow1 == 1):
        enemyFind.append({'x' : e1x, 'y' : e1y})
    if (enemyShow2 == 1):
        enemyFind.append({'x' : e2x, 'y' : e2y})
    if (enemyShow3 == 1):
        enemyFind.append({'x' : e3x, 'y' : e3y})

    
    if (abs(x - 500) <= 125 and int(Angle * 45) != 90):
        if (int(Angle * 45) > 90):
            return "TURN_RIGHT"
        else:
            return "TURN_LEFT"
    if (len(enemyFind) != 0):
        if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
            
            return random.choice(["FORWARD", "BACKWARD", "SHOOT"])
        
        return TurnAngleToEnemy_(x, y, gunAngle * 45, enemyFind, hitTmDis)

    WallAction = ShootWall(gunAngle * 45, wallLeft, wallRight, wallUp, wallDown)

    if (WallAction != "MEOW"):
        return WallAction
    
    if (abs(x - 500) > 125):
        return "FORWARD"

    
    return random.choice(["FORWARD", "BACKWARD"])

def TurnAngleToEnemy_(selfX, selfY, gunAngle, enemyFind, teamMateShootDis):
    targetX, targetY = getMinDisOppo_(selfX, selfY, enemyFind)
    
    dis = getDistance(selfX, selfY, targetX, targetY)

    targetAngleGap = getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis)

    if (np.cos(targetAngleGap / 180 * np.pi) >= 1 / (2 ** 0.5)):
        return random.choice(["FORWARD", "BACKWARD"])
    
    elif (np.sin(targetAngleGap / 180 * np.pi) < 0):
        return "AIM_LEFT"
    else:
        return "AIM_RIGHT"
    
def getMinDisOppo_(selfX, selfY, enemyFind):
    competitorData = enemyFind

    targetX = 1e4
    targetY = 1e4
    for c in competitorData:
        competitorX = c['x']
        competitorY = c['y']

        if (getDistance(targetX, targetY, selfX, selfY) > getDistance(competitorX, competitorY, selfX, selfY)):
            targetX = competitorX
            targetY = competitorY
    return targetX, targetY

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