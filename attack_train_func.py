from battle import *
from util import *
from battleAlgorithm import *
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

    #e1HP, e2HP, e3HP = enemy_info[0]['lives'], enemy_info[1]['lives'], enemy_info[2]['lives']

    return [x, y, Angle, gunAngle, hitTmDis, wallUp, walldown, wallLeft, wallRight,
             e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow[0], enemyShow[1], enemyShow[2]]



def isAimToYou(selfX, selfY, gunAngle, targetX, targetY, teamMateShootDis):
    dis = getDistance(selfX, selfY, targetX, targetY)
    action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
    if (dis > teamMateShootDis and dis < 300):#dis > teamMateShoot代表會射到隊友
        return -1
    if (action == "NONE"):
        return 0
    return 1


def rewardFunction(DataForAgent, action, score, livesLoss):
    reward = livesLoss * (-10) + getScoreReward(score)

    x, y, Angle, gunAngle, hitTmDis, wallUp, wallDown, wallLeft, wallRight,\
    e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(DataForAgent)

    enemyFind = []

    if (enemyShow1 == 1):
        enemyFind.append({'x' : e1x, 'y' : e1y})
    if (enemyShow2 == 1):
        enemyFind.append({'x' : e2x, 'y' : e2y})
    if (enemyShow3 == 1):
        enemyFind.append({'x' : e3x, 'y' : e3y})

    if (action == "SHOOT"):
        if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
            reward += 0.5
        elif (e1Aim == -1 or e2Aim == -1 or e3Aim == -1):
            reward -= 2

    elif (len(enemyFind) != 0 and (action == "AIM_RIGHT" or action == "AIM_LEFT")):
        aimAction = TurnAngleToEnemy_(x, y, gunAngle * 45, enemyFind, hitTmDis)
        if (aimAction == action):
            reward += 0.5

    elif (ShootWall(gunAngle * 45, wallLeft, wallRight, wallUp, wallDown) == action):
        reward += 0.0001

    return reward




def getScoreReward(score):
    reward = 0
    if (score >= 20):
        reward += int(score / 20) * 10 #打到人10分
        score = score % 20

    if (score >= 5):
        reward += int(score / 5) * 0.001 #打爆牆壁0.02分
        score = score % 5

    return reward + score * 0.001
        