
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

    

    e1Aim, e2Aim, e3Aim = isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e1x, e1y, hitTmDis) * int(enemy_info[0]['lives'] != 0), \
                            isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e2x, e2y, hitTmDis) * int(enemy_info[1]['lives'] != 0),\
                            isAimToYou(x, y, (data['gun_angle'] + 540) % 360, e3x, e3y, hitTmDis) * int(enemy_info[2]['lives'] != 0)
    
    e1Dis = min(getDistance(e1x, e1y, x, y) + int(enemy_info[0]['lives'] == 0) * 1300, 1300)
    e2Dis = min(getDistance(e2x, e2y, x, y) + int(enemy_info[1]['lives'] == 0) * 1300, 1300)
    e3Dis = min(getDistance(e3x, e3y, x, y) + int(enemy_info[2]['lives'] == 0) * 1300, 1300)

    e1Angle = getTargetAngle(0, 0, e1x - x, e1y - y, e1Dis)
    e2Angle = getTargetAngle(0, 0, e2x - x, e2y - y, e2Dis)
    e3Angle = getTargetAngle(0, 0, e3x - x, e3y - y, e3Dis)


    return [Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis]

def normalizeData(DataForAgent):
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis = tuple(DataForAgent)

    return Angle / 8, gunAngle / 8, e1Angle / 360, e2Angle / 360, e3Angle / 360, \
        e1Aim, e2Aim, e3Aim, e1Dis / 1300, e2Dis / 1300, e3Dis / 1300

    #加上distance的資訊




def rewardFunction(DataForAgent, action : str, score, livesLoss):
    reward = score / 10 + livesLoss * 2

    

    predict = coach(DataForAgent)

    if (action in predict):
        return reward + 0.01
    else:
        return reward + -0.01
    #Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis = tuple(DataForAgent)

    # Angle *= 45
    # gunAngle *= 45


    # enemyAngle = []
    # if (e1Dis <= 1200):
    #     enemyAngle.append((e1Angle, e1Dis))
    # if (e2Dis <= 1200):
    #     enemyAngle.append((e2Angle, e2Dis))
    # if (e3Dis <= 1200):
    #     enemyAngle.append((e3Angle, e3Dis))

    # minDisEnemyAngle, minEnemyDis = GetMinDisEnemy(gunAngle, enemyAngle)
    # targetGunAngleGap = gunAngle - minDisEnemyAngle
    # targetTankAngleGap = (Angle - (int((minDisEnemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360


    # if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
    #     if (action == "SHOOT"):
    #         reward += 1
    #     elif ()

    # elif (action == "SHOOT"):
    #     if (e1Aim == -1 or e2Aim == -1 or e3Aim == -1):
    #         reward -= 10
    #     else:
    #         reward -= 0.5
    
    # if (minEnemyDis <= 300):
        
    #     if (np.cos(targetGunAngleGap / 180 * np.pi) >= 1 / (2 ** 0.5)):
    #         reward += 0.05
    #     else:
    #         reward -= 0.03
    #     if (targetTankAngleGap % 180 != 0 and targetTankAngleGap % 90 == 0):
    #         reward += 0.05
    #     else:
    #         reward -= 0.03
    


    return reward

def coach(dataForAgent)->list:
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis = tuple(dataForAgent)
    
    if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
        return ["FORWARD", "BACKWARD", "SHOOT"]

    enemyAngle = []
    if (e1Dis <= 1200):
        enemyAngle.append((e1Angle, e1Dis))
    if (e2Dis <= 1200):
        enemyAngle.append((e2Angle, e2Dis))
    if (e3Dis <= 1200):
        enemyAngle.append((e3Angle, e3Dis))

    minDisEnemyAngle, minEnemyDis = GetMinDisEnemy(gunAngle, enemyAngle)
    if (minEnemyDis <= 300):
        return meetEnemyForReward(Angle * 45, gunAngle * 45, minDisEnemyAngle)
    else:
        return [moveToEnemy(Angle * 45, minDisEnemyAngle)]

def meetEnemyForReward(tankAngle, gunAngle, enemyAngle):
    targetGunAngleGap = gunAngle - enemyAngle
    targetTankAngleGap = (tankAngle - (int((enemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360
    if (np.cos(targetGunAngleGap / 180 * np.pi) >= 1 / (2 ** 0.5)):
        if (targetTankAngleGap % 180 == 0 or targetTankAngleGap % 180 == 135):
            return ["TURN_RIGHT"]
        elif (targetTankAngleGap % 180 == 45):
            return ["TURN_LEFT"]
        else:
            return ["FORWARD", "BACKWARD"]
    
    elif (np.sin(targetGunAngleGap / 180 * np.pi) < 0):
        return ["AIM_LEFT"]
    else:
        return ["AIM_RIGHT"]
def GetMinDisEnemy(gunAngle, enemyAngleDis):
    enemyAngle = gunAngle
    minEnemyDis = 1e4
    for angle, dis in enemyAngleDis:
        if (dis < minEnemyDis):
            minEnemyDis = dis
            enemyAngle = angle
    return enemyAngle, minEnemyDis

def meetEnemy(tankAngle, gunAngle, enemyAngle):
    targetGunAngleGap = gunAngle - enemyAngle
    targetTankAngleGap = (tankAngle - (int((enemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360
    if (np.cos(targetGunAngleGap / 180 * np.pi) >= 1 / (2 ** 0.5)):
        if (targetTankAngleGap % 180 == 0 or targetTankAngleGap % 180 == 135):
            return "TURN_RIGHT"
        elif (targetTankAngleGap % 180 == 45):
            return "TURN_LEFT"
        else:
            return random.choice(["FORWARD", "BACKWARD"])
    
    elif (np.sin(targetGunAngleGap / 180 * np.pi) < 0):
        return "AIM_LEFT"
    else:
        return "AIM_RIGHT"
    
def moveToEnemy(tankAngle, enemyAngle):
    targetTankAngleGap = (tankAngle - (int((enemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360

    if (targetTankAngleGap == 0):
        return "FORWARD"
    elif (targetTankAngleGap == 180):
        return "BACKWARD"
    else:
        return "TURN_RIGHT"
