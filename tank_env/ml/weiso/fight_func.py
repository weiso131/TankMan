
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from usefulFunction import *




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
    power = data['power']
      

    e1Aim, e2Aim, e3Aim = isAimToYou(x, y, gunAngle, e1x, e1y, hitTmDis, enemy_info[0]['lives'], cooldown) * int(power != 0), \
                            isAimToYou(x, y, gunAngle, e2x, e2y, hitTmDis, enemy_info[1]['lives'], cooldown) * int(power != 0),\
                            isAimToYou(x, y, gunAngle, e3x, e3y, hitTmDis, enemy_info[2]['lives'], cooldown) * int(power != 0) 
    
    e1Dis = min(getDistance(e1x, e1y, x, y) + int(enemy_info[0]['lives'] == 0) * 1300, 1300)
    e2Dis = min(getDistance(e2x, e2y, x, y) + int(enemy_info[1]['lives'] == 0) * 1300, 1300)
    e3Dis = min(getDistance(e3x, e3y, x, y) + int(enemy_info[2]['lives'] == 0) * 1300, 1300)

    e1Angle = getTargetAngle(0, 0, e1x - x, e1y - y, e1Dis)
    e2Angle = getTargetAngle(0, 0, e2x - x, e2y - y, e2Dis)
    e3Angle = getTargetAngle(0, 0, e3x - x, e3y - y, e3Dis)


    return [Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis, avoidDirect]

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

def rader(x, y, graph:list):
    raderGraph = graph.copy()

    graphX, graphY = int(x / 25), int(y / 25)
    xMax, xMin = min(39, graphX + 12), max(-1, graphX - 12)

    for i in range(graphY, min(23, graphY + 12)):
        if (raderGraph[i, graphX] == 1): break
        for j in range(graphX, xMax):
            if (raderGraph[i, j] == 1): 
                xMax = j - 1
                break
            raderGraph[i, j] = 6
        for j in range(graphX, xMin, -1):
            if (raderGraph[i, j] == 1):
                xMin = j + 1
                break
            raderGraph[i, j] = 6

    xMax, xMin = min(39, graphX + 12), max(-1, graphX - 12)
    for i in range(graphY, max(-1, graphY - 12), -1):
        if (raderGraph[i, graphX] == 1): break
        for j in range(graphX, xMax):
            if (raderGraph[i, j] == 1): 
                xMax = j - 1
                break
            raderGraph[i, j] = 6
        for j in range(graphX, xMin, -1):
            if (raderGraph[i, j] == 1):
                xMin = j + 1
                break
            raderGraph[i, j] = 6

    return raderGraph
        
def seeEnemy(data, graph):
    x, y, _, _ = getTank(data)
    raderGraph = rader(x, y, graph)
    for enemy in data["competitor_info"]:
        enemyAngle = (enemy['angle'] + 540) % 360
        enemyX, enemyY = enemy['x'] + 12.5 - 5 * int(enemyAngle % 90 != 0), enemy['y'] + 12.5 - 5 * int(enemyAngle % 90 != 0)
        if (raderGraph[int(enemyY / 25), int(enemyX / 25)]):
            return True

    return False

def enemySameSide(data):
    x, y, _, _ = getTank(data)
    targetX, targetY = -1000, -1000
    for enemy in data["competitor_info"]:
        enemyAngle = (enemy['angle'] + 540) % 360
        enemyX = enemy['x'] + 12.5 - 5 * int(enemyAngle % 90 != 0)
        if (((x > 500 and enemyX > 500) or (x <= 500 and enemyX <= 500)) and \
            getDistance(enemyX, enemyX, x, y) < getDistance(targetX, targetY, x, y)):
            targetX, targetY = enemyX, enemyX
    return targetX, targetY

def getBullet(data : dict, bullet_history : dict, graph : np.ndarray):
    bullet_info = data["bullets_info"]

    existBullet = []

    for b in bullet_info:
        id = b["id"]
        startX, startY = b['x'], b['y']
        existBullet.append(id)
        if (bullet_history[id][0] == -1):
            
            angle = (b['rot'] + 540 ) %  360
            cos, sin = PosNag(np.cos(angle / 180 * np.pi)), PosNag(np.sin(angle / 180 * np.pi))

            if (angle % 90 == 0):
                endX, endY = startX + 330 * cos, startY - 330 * sin
            else:
                endX, endY = startX + 231 * cos, startY - 231 * sin
            bullet_history[id] = (startX, startY, max(0, min(endX, 999)), max(0, min(endY, 599)), angle)
        
        _, _, endX, endY, _ = bullet_history[id]

        graph = drawBullet(startX, startY, endX, endY, graph, int(id[0]))
    
    #刪除過期的子彈資料
    for i in range(1, 7):
        key = str(i) + 'P_bullet'
        if (not (key in existBullet)):
            bullet_history[key] = (-1, -1, -1, -1, -1)

    return bullet_history, graph

def drawBullet(startX, startY, endX, endY, graph, id : int):
    wayX, wayY = PosNag(endX - startX), -PosNag(endY - startY)

    graphStartX, graphStartY = int(startX / 25), int(startY / 25)
    graphEndX, graphEndY = int(endX / 25), int(endY / 25)

    step = 0
    while ((graphStartX + step * wayX != graphEndX + wayX or \
            graphStartX == graphEndX) and \
           (graphStartY + step * wayY != graphEndY + wayY or
            graphStartY == graphEndY)):
        x = graphStartX + step * wayX
        y = graphStartY + step * wayY
        if (graph[y, x] == 1):
            break
        graph[y, x] = -id

        step += 1
    return graph

def avoidBullet(value, angle, bullet_history, avoidDirect):
    """
    value是代表這個子彈路徑所顯示的值(-id)
    """


    bullet_angle = bullet_history[str(-int(value)) + "P_bullet"][4]

    angleGap = (angle - bullet_angle + 360) % 360

    if (angleGap % 180 == 90):
        if (avoidDirect == 0):
            return "FORWARD"
        else:
            return "BACKWARD"
    elif (angleGap % 180 == 135):
        return "TURN_RIGHT"
    else:
        return "TURN_LEFT"

