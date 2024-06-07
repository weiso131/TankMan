from util import *
import random




def Shoot(selfX, selfY, gunAngle, targetX, targetY, dis):
    angleGap = abs(getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis))
    angleTan = np.tan(angleGap / 180 * np.pi)

    if (np.cos(angleGap / 180 * np.pi) >= 1 / (2 ** 0.5) and abs(dis * angleTan) < 25 and dis < 300):
        return "SHOOT"
    return "NONE"

def getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis):
    target_vec_cos = getXVec(selfX, targetX) / dis
    target_vec_sin = getYVec(selfY, targetY) / dis

    targetAngle = (np.degrees(np.arctan2(target_vec_sin, target_vec_cos)) + 360) % 360

    return gunAngle - targetAngle

    
def shootTeamMate(data, selfX, selfY, gunAngle):
    """
    確認這個砲口方向會不會打到隊友
    """
    teamMateShoot = 600
    for tm in data['teammate_info']:
        if (tm['id'] == data['id']):
            continue
        if ((tm['x'] != selfX or tm['y'] != selfY) and tm['lives'] > 0):
            tmDis = getDistance(selfX, selfY, tm['x'], tm['y'])
            
            if (Shoot(selfX, selfY, gunAngle, tm['x'], tm['y'], tmDis) == "SHOOT" and tmDis < teamMateShoot):
                teamMateShoot = tmDis  
    return teamMateShoot




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
        wallThisAngle = haveWall(graph, graphX, graphY, horizon_angle)
        if (wallThisAngle <= 300 and wallThisAngle < shootTeamMate(data, x, y, horizon_angle) ):
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
