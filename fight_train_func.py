
from attack_train_func import *
"""
訓練場地必須是沒有任何方塊
殺紅眼的戰車
"""

def getDataForAgent(data, graph, avoidDirect):



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


    return [Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis, avoidDirect]

def normalizeData(DataForAgent):
    targetAngleDiscrete, AngleDiscrete, gunAngleDiscrete, Aim, minDistanceDiscrete = getQTableData(DataForAgent)

    return targetAngleDiscrete / 7, AngleDiscrete / 7, gunAngleDiscrete / 7, Aim / 2, minDistanceDiscrete / 1


def getQTableData(DataForAgent):
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis, avoidDirect = tuple(DataForAgent)
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

    Aim = 0 #0會打到隊友，1沒事，2會打到敵人
    if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
        Aim = 1

    minDistanceDiscrete = 0 #0代表有人在範圍內，1代表沒人
    if (minEnemyDis > 300):
        minDistanceDiscrete = 1


    return targetAngleDiscrete, AngleDiscrete, gunAngleDiscrete, Aim, minDistanceDiscrete, avoidDirect


def rewardFunction(DataForAgent, action : str, score, livesLoss):
    reward = 0
    predict = coach(DataForAgent)

    if (action in predict):
        return reward + 0.01
    else:
        return reward + -0.01
      

def coach(dataForAgent)->list:
    #注意角度
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis, avoidDirect = tuple(dataForAgent)
    
    if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
        return ["SHOOT"]

    enemyAngle = []
    if (e1Dis <= 1200):
        enemyAngle.append((e1Angle, e1Dis))
    if (e2Dis <= 1200):
        enemyAngle.append((e2Angle, e2Dis))
    if (e3Dis <= 1200):
        enemyAngle.append((e3Angle, e3Dis))

    minDisEnemyAngle, minEnemyDis = GetMinDisEnemy(gunAngle, enemyAngle)
    if (minEnemyDis <= 300):
        return meetEnemyForReward(Angle, gunAngle, minDisEnemyAngle, avoidDirect)
    else:
        return [moveToEnemy(Angle, minDisEnemyAngle)]

def meetEnemyForReward(tankAngle, gunAngle, enemyAngle, avoidDirect):
    targetGunAngleGap = gunAngle - enemyAngle
    targetTankAngleGap = (tankAngle - (int((enemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360
    if (np.cos(targetGunAngleGap / 180 * np.pi) >= 3 ** 0.5 / 2):
        if (targetTankAngleGap % 180 == 0 or targetTankAngleGap % 180 == 135):
            return ["TURN_RIGHT"]
        elif (targetTankAngleGap % 180 == 45):
            return ["TURN_LEFT"]
        elif (avoidDirect == 0):
            return ["FORWARD"]
        else:
            return ["BACKWARD"]
    
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

def meetEnemy(tankAngle, gunAngle, enemyAngle, avoidDirect):
    targetGunAngleGap = gunAngle - enemyAngle
    targetTankAngleGap = (tankAngle - (int((enemyAngle + 22.5) / 45) % 8) * 45 + 360) % 360
    if (np.cos(targetGunAngleGap / 180 * np.pi) >= 3 ** 0.5 / 2):
        if (targetTankAngleGap % 180 == 0 or targetTankAngleGap % 180 == 135):
            return "TURN_RIGHT"
        elif (targetTankAngleGap % 180 == 45):
            return "TURN_LEFT"
        elif (avoidDirect == 0):
            return "FORWARD"
        else:
            return "BACKWARD"
    
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
    

def graphThisAngle(x, y, angle, graph):
    """
    angle : 0, 45, 90, ...

    return: 走幾步碰到邊界或牆壁
    """
    cos, sin = PosNag(np.cos(angle / 180 * np.pi)), -PosNag(np.sin(angle / 180 * np.pi))

    graphX, graphY = int(x / 25), int(y / 25)

    step = 1


    if (angle % 90 == 0):   
        while (step * cos + graphX < 40 and step * cos + graphX >= 0 and\
               step * sin + graphY < 24 and step * sin + graphY >= 0):
            
            if (graph[step * sin + graphY, step * cos + graphX] != 0):
                break

            if (graphX + sin < 40 and graphX + sin >= 0 and\
                graphY + cos < 24 and graphY + cos >= 0 and\
                graph[step * sin + graphY + cos, step * cos + graphX + sin] != 0 and\
                graph[graphY + cos, graphX + sin] == 0):
                break
            if (graphX - sin < 40 and graphX - sin >= 0 and\
                graphY - cos < 24 and graphY - cos >= 0 and\
                graph[step * sin + graphY - cos, step * cos + graphX - sin] != 0 and\
                graph[graphY - cos, graphX - sin] == 0):
                break
            step += 1

    else:
        while (step * cos + graphX < 40 and step * cos + graphX >= 0 and\
               step * sin + graphY < 24 and step * sin + graphY >= 0):
            
            if (graph[step * sin + graphY, step * cos + graphX] != 0):
                break
            if (step != 0 and graph[step * sin + graphY , step * cos + graphX - cos] != 0):
                break
            if (step != 0 and graph[step * sin + graphY - sin, step * cos + graphX] != 0):
                break
            step += 1

    return step
