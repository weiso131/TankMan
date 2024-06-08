
from attack_train_func import *

"""
訓練場地必須是沒有任何方塊
殺紅眼的戰車
"""

def getDataForAgent(data, graph):
    Angle = ((data['angle'] + 540) % 360) / 45
    x = data['x'] + 12.5 + 5 * (Angle * 45 % 90 != 0)
    y = data['y'] + 12.5 + 5 * (Angle * 45 % 90 != 0)
    
    gunAngle = ((data['gun_angle'] + 540) % 360) / 45
    hitTmDis = shootTeamMate(data, x, y, (data['gun_angle'] + 540) % 360)
    

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

    return [Angle, gunAngle, e1x - x, e1y - y, e2x - x, e2y - y, e3x - x, e3y - y, e1Aim, e2Aim, e3Aim, enemyShow[0], enemyShow[1], enemyShow[2]]

def normalizeData(DataForAgent):
    Angle, gunAngle, e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(DataForAgent)

    e1Dis = (e1x ** 2 + e1y ** 2) ** 0.5 + 1e-7
    e2Dis = (e2x ** 2 + e2y ** 2) ** 0.5 + 1e-7
    e3Dis = (e3x ** 2 + e3y ** 2) ** 0.5 + 1e-7

    return Angle / 8, gunAngle / 8, e1x / e1Dis, e1y / e1Dis, e2x / e2Dis, e2y / e2Dis, e3x / e3Dis, e3y / e3Dis, \
        (e1Aim + 1) / 2, (e2Aim + 1) / 2, (e3Aim + 1) / 2, enemyShow1, enemyShow2, enemyShow3, min(e1Dis, 300) / 300, min(e2Dis, 300) / 300, min(e3Dis, 300) / 300

    #加上distance的資訊




def rewardFunction(DataForAgent, action : str, score, livesLoss):
    reward = livesLoss * (-10) + score / 2

    Angle, gunAngle, e1x, e1y, e2x, e2y, e3x, e3y, \
        e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(DataForAgent)

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
            reward -= 10

    elif (len(enemyFind) != 0 and (action == "AIM_RIGHT" or action == "AIM_LEFT")):
        aimAction = TurnAngleToEnemy_(0, 0, gunAngle * 45, enemyFind)
        if (aimAction == action):
            reward += 0.5
        else:
            reward -= 0.5


    return reward



