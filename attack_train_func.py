from battle import *
from util import *
def getDataForAgent(data, graph):
    Angle = ((data['angle'] + 540) % 360) / 45
    x = data['x'] + 12.5 + 5 * (Angle * 45 % 90 != 0)
    y = data['y'] + 12.5 + 5 * (Angle * 45 % 90 != 0)
    
    gunAngle = ((data['gun_angle'] + 540) % 360) / 45
    hitTmDis = shootTeamMate(data, x, y, (data['gun_angle'] + 540) % 360)
    
    wallRight, wallUp,  wallLeft, walldown = haveWallFourWay(data, x, y, graph)

    enemy_info = data['competitor_info']

    e1x, e1y = enemy_info[0]['x'] + 12.5 + 5 * (enemy_info[0]['angle'] % 90 != 0), enemy_info[0]['y'] + 12.5 + 5 * (enemy_info[0]['angle'] % 90 != 0)
    e2x, e2y = enemy_info[1]['x'] + 12.5 + 5 * (enemy_info[1]['angle'] % 90 != 0), enemy_info[1]['y'] + 12.5 + 5 * (enemy_info[1]['angle'] % 90 != 0)
    e3x, e3y = enemy_info[2]['x'] + 12.5 + 5 * (enemy_info[2]['angle'] % 90 != 0), enemy_info[2]['y'] + 12.5 + 5 * (enemy_info[2]['angle'] % 90 != 0)

    

    e1Aim, e2Aim, e3Aim = isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e1x, e1y, hitTmDis), \
                            isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e2x, e2y, hitTmDis),\
                            isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e3x, e3y, hitTmDis)
    
    enemyShow = [0, 0, 0]
    enemyFind = enemyReach(graph, data)

    for enemy in enemyFind:
        id = (int(enemy['id'][0]) - 1) % 3
        enemyShow[id] = 1

    e1HP, e2HP, e3HP = enemy_info[0]['lives'], enemy_info[1]['lives'], enemy_info[2]['lives']

    return [x, y, Angle, gunAngle, hitTmDis, wallUp, walldown, wallLeft, wallRight,
             e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow[0], enemyShow[1], enemyShow[2], e1HP, e2HP, e3HP]

def testDataForAgent(dataForAgent):
    x, y, Angle, gunAngle, hitTmDis, wallUp, wallDown, wallLeft, wallRight,\
    e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3, e1HP, e2HP, e3HP = tuple(dataForAgent)
    
    enemyFind = []

    if (enemyShow1 == 1):
        enemyFind.append({'x' : e1x, 'y' : e1y})
    if (enemyShow2 == 1):
        enemyFind.append({'x' : e2x, 'y' : e2y})
    if (enemyShow3 == 1):
        enemyFind.append({'x' : e3x, 'y' : e3y})

    if (abs(x - 500) > 125):
        return "FORWARD"
    elif (int(Angle * 45) != 90):
        if (int(Angle * 45) > 90):
            return "TURN_RIGHT"
        else:
            return "TURN_LEFT"
    
    if (len(enemyFind) != 0):
        if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
            return random.choice(["FORWARD", "BACKWARD", "SHOOT"])
        
        return TurnAngleToEnemy_(x, y, gunAngle * 45, enemyFind, hitTmDis)

    if (wallLeft == 1):
        return turnGunToWall(gunAngle * 45, 180)
    if (wallRight == 1):
        return turnGunToWall(gunAngle * 45, 0)
    if (wallUp == 1): 
        return turnGunToWall(gunAngle * 45, 90)
    if (wallDown == 1):
        return turnGunToWall(gunAngle * 45, 270)



    return random.choice(["FORWARD", "BACKWARD"])

def isAimToYou(selfX, selfY, gunAngle, targetX, targetY, teamMateShootDis):
    dis = getDistance(selfX, selfY, targetX, targetY)
    action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
    if (dis > teamMateShootDis or action == "NONE"):#dis > teamMateShoot代表會射到隊友
        return 0
    return 1

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

def turnGunToWall(gunAngle, wallAngle):
    if (gunAngle == wallAngle):
        return "SHOOT"
    elif (gunAngle > wallAngle):
        return "AIM_RIGHT"
    else:
        return "AIM_LEFT"