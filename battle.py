from util import *
import random
def getMinDisOppo(data, enemyFind):
    selfX = data['x']
    selfY = data['y']
    competitorData = enemyFind

    targetX = 1e4
    targetY = 1e4
    for c in competitorData:
        competitorX = c['x']
        competitorY = c['y']

        if (getDistance(targetX, targetY, selfX, selfY) > getDistance(competitorX, competitorY, selfX, selfY) and c['lives'] > 0):
            targetX = competitorX + 12.5 + 5 * int(c['angle'] % 90 == 0)
            targetY = competitorY + 12.5 + 5 * int(c['angle'] % 90 == 0)
    return targetX, targetY


def getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis):
    target_vec_cos = getXVec(selfX, targetX) / dis
    target_vec_sin = getYVec(selfY, targetY) / dis

    targetAngle = (np.degrees(np.arctan2(target_vec_sin, target_vec_cos)) + 360) % 360

    return gunAngle - targetAngle
def Shoot(selfX, selfY, gunAngle, targetX, targetY, dis):
    angleGap = abs(getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis))
    angleTan = np.tan(angleGap / 180 * np.pi)

    if (angleGap <= 45 and dis * angleTan < 13 and dis < 300):
        return "SHOOT"
    return "NONE"
def TurnAngleToTarget(data, enemyFind):
    targetX, targetY = getMinDisOppo(data, enemyFind)
    selfX = data['x'] + 5 * int(data['angle'] % 90 != 0) + 12.5
    selfY = data['y'] + 5 * int(data['angle'] % 90 != 0) + 12.5
    gunAngle = (data['gun_angle'] + 540) % 360
    dis = getDistance(selfX, selfY, targetX, targetY)

    targetAngleGap = getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis)


    #檢查在這個炮口路徑上，子彈飛多遠會打到隊友
    teamMateShootDis = shootTeamMate(data, selfX, selfY, gunAngle)

    
    if (np.cos(targetAngleGap / 180 * np.pi) >= 1 / (2 ** 0.5)):
        action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
        if (dis > teamMateShootDis or dis > 300):#dis > teamMateShoot代表會射到隊友
            return random.choice(["FORWARD", "BACKWARD"])
        if (action == "NONE"):
            return random.choice(["FORWARD", "BACKWARD", "SHOOT"])
        return action
    
    elif (np.sin(targetAngleGap / 180 * np.pi) < 0):
        return "AIM_LEFT"
    else:
        return "AIM_RIGHT"
    
def shootTeamMate(data, selfX, selfY, gunAngle):
    """
    確認這個砲口方向會不會打到隊友
    """
    teamMateShoot = 600
    for tm in data['teammate_info']:
        if ((tm['x'] != selfX or tm['y'] != selfY) and tm['lives'] > 0):
            tmDis = getDistance(selfX, selfY, tm['x'], tm['y'])
            tmAngleGap = getTargetAngleGap(selfX, selfY, gunAngle, tm['x'], tm['y'], tmDis)
            if (abs(tmAngleGap) <= 45 and Shoot(selfX, selfY, gunAngle=gunAngle, targetX=tm['x'], targetY=tm['y'], dis=tmDis) == "SHOOT" and tmDis < teamMateShoot):
                teamMateShoot = tmDis  
    return teamMateShoot


def fight(graph, data):
    


    gunAngle = (data['gun_angle'] + 540) % 360
    angle = (data['angle'] + 540) % 360
    
    x, y = data['x'] + 5 * int(angle % 90 != 0) + 12.5, data['y'] + 5 * int(angle % 90 != 0) + 12.5 #方位補正，轉到斜的座標會-5
    graphX, graphY = int(x / 25), int(y / 25)
    
    if (abs(x - 500) > 125):
        return "FORWARD"
    elif (angle != 90):
        if (angle > 90):
            return "TURN_RIGHT"
        else:
            return "TURN_LEFT"
    enemyFind = enemyReach(graph, data)
    if (len(enemyFind) != 0):
        return TurnAngleToTarget(data, enemyFind)

    wallFourWay = haveWallFourWay(data, x, y, graph)
    for i in range(4):
        wall = wallFourWay[i]
        if (wall == 1):
            if (gunAngle == i * 90):
                return "SHOOT"
            elif (gunAngle > i * 90):
                return "AIM_RIGHT"
            else:
                return "AIM_LEFT"
     
    return random.choice(["FORWARD", "BACKWARD"])



def PosNag(num):
    """
    正值回傳:1
    負值回傳:-1
    否則:0
    """
    if (abs(num) < 1e-9):
        return 0
    elif (num > 0):
        return 1
    elif (num < 0):
        return -1

def haveWallFourWay(data, x, y, graph):
    """
    這個方向有沒有牆可以打
    """
    fourWay = []
    graphX, graphY = int(x / 25), int(y / 25)
    for horizon_angle in range(0, 360, 90):
        teamMateShootDis = shootTeamMate(data, x, y, horizon_angle)
        wallThisAngle = haveWall(graph, graphX, graphY, horizon_angle)
        if (wallThisAngle <= 300 and wallThisAngle < teamMateShootDis ):
            fourWay.append(1)
        else:
            fourWay.append(0)
    return tuple(fourWay)

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
    return 600


def enemyReach(graph, data):
    x, y = data['x'] + 12.5 + 5 * int(data['angle'] % 90 == 0), data['y'] + 12.5 + 5 * int(data['angle'] % 90 == 0)
    competitor_info = data['competitor_info']

    enemyFind = []
    for enemy in competitor_info:
        enemy_x, enemy_y = enemy['x'] + 12.5 + 5 * int(enemy['angle'] % 90 == 0), enemy['y'] + 12.5 + 5 * int(enemy['angle'] % 90 == 0)
        enemyWayX, enemyWayY = PosNag(enemy_x - x) + 1 - abs(PosNag(enemy_x - x)), PosNag(enemy_y - y) + 1 - abs(PosNag(enemy_y - y))

        seeEnemy = True

        for wall_x in range(int(x / 25), int(enemy_x / 25), enemyWayX):
            for wall_y in range(int(y / 25), int(enemy_y / 25), enemyWayY):
                if (int(graph[wall_y, wall_x]) > 0):
                    seeEnemy = False
                    break
            if (not seeEnemy): break

        if (seeEnemy and enemy['lives'] > 0):
            enemyFind.append(enemy)
    return enemyFind

