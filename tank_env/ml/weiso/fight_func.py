
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from usefulFunction import *




def getDataForAgent(data, graph):



    Angle = (data['angle'] + 540) % 360
    x = data['x'] + 12.5 + 5 * (Angle % 90 != 0)
    y = data['y'] + 12.5 + 5 * (Angle % 90 != 0)
    
    gunAngle = (data['gun_angle'] + 540) % 360
    hitTmDis = shootTeamMate(data, x, y, gunAngle)
    

    enemy_info = data['competitor_info']

    e1x, e1y = enemy_info[0]['x'] + 12.5 + 5 * (enemy_info[0]['angle'] % 90 != 0), enemy_info[0]['y'] + 12.5 + 5 * (enemy_info[0]['angle'] % 90 != 0)
    e2x, e2y = enemy_info[1]['x'] + 12.5 + 5 * (enemy_info[1]['angle'] % 90 != 0), enemy_info[1]['y'] + 12.5 + 5 * (enemy_info[1]['angle'] % 90 != 0)
    e3x, e3y = enemy_info[2]['x'] + 12.5 + 5 * (enemy_info[2]['angle'] % 90 != 0), enemy_info[2]['y'] + 12.5 + 5 * (enemy_info[2]['angle'] % 90 != 0)


    cooldown = data['cooldown']
      

    e1Aim, e2Aim, e3Aim = isAimToYou(x, y, gunAngle, e1x, e1y, hitTmDis, enemy_info[0]['lives'], cooldown), \
                            isAimToYou(x, y, gunAngle, e2x, e2y, hitTmDis, enemy_info[1]['lives'], cooldown),\
                            isAimToYou(x, y, gunAngle, e3x, e3y, hitTmDis, enemy_info[2]['lives'], cooldown) 
    
    e1Dis = min(getDistance(e1x, e1y, x, y) + int(enemy_info[0]['lives'] == 0) * 1300, 1300)
    e2Dis = min(getDistance(e2x, e2y, x, y) + int(enemy_info[1]['lives'] == 0) * 1300, 1300)
    e3Dis = min(getDistance(e3x, e3y, x, y) + int(enemy_info[2]['lives'] == 0) * 1300, 1300)

    e1Angle = getTargetAngle(0, 0, e1x - x, e1y - y, e1Dis)
    e2Angle = getTargetAngle(0, 0, e2x - x, e2y - y, e2Dis)
    e3Angle = getTargetAngle(0, 0, e3x - x, e3y - y, e3Dis)


    return [Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis]

def getQTableData(DataForAgent):
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis = tuple(DataForAgent)
    enemyAngle = []
    if (e1Dis <= 1200):
        enemyAngle.append((e1Angle, e1Dis))
    if (e2Dis <= 1200):
        enemyAngle.append((e2Angle, e2Dis))
    if (e3Dis <= 1200):
        enemyAngle.append((e3Angle, e3Dis))

    minDisEnemyAngle, minEnemyDis = GetMinDisEnemy(gunAngle, enemyAngle)

    targetAngleDiscrete = int((minDisEnemyAngle + 22.5) / 45) % 8 #0 ~ 7
    AngleDiscrete = int(Angle / 45) % 8 #0 ~ 7
    gunAngleDiscrete = int(gunAngle / 45) % 8 #0 ~ 7

    Aim = 1 #0會打到隊友，1沒事，2會打到敵人
    if (e1Aim == -1 or e2Aim == -1 or e3Aim == -1):
        Aim = 0
    elif (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
        Aim = 2

    minDistanceDiscrete = 0 #0代表有人在範圍內，1代表沒人
    if (minEnemyDis > 300):
        minDistanceDiscrete = 1


    return targetAngleDiscrete, AngleDiscrete, gunAngleDiscrete, Aim, minDistanceDiscrete

def GetMinDisEnemy(gunAngle, enemyAngleDis):
    
    enemyAngle = gunAngle
    minEnemyDis = 1e4
    for angle, dis in enemyAngleDis:
        if (dis < minEnemyDis):
            minEnemyDis = dis
            enemyAngle = angle
    return enemyAngle, minEnemyDis


def isAimToYou(selfX, selfY, gunAngle, targetX, targetY, teamMateShootDis, lives, cooldown):
    dis = getDistance(selfX, selfY, targetX, targetY)
    action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
    if ((dis > teamMateShootDis and dis < 300) or cooldown != 0):#dis > teamMateShoot代表會射到隊友
        return -1
    if (action == "NONE" or lives == 0):
        return 0
    return 1







