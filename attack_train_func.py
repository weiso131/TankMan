from util import *
import random




def isAimToYou(selfX, selfY, gunAngle, targetX, targetY, teamMateShootDis, lives, cooldown):
    dis = getDistance(selfX, selfY, targetX, targetY)
    action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
    if ((dis > teamMateShootDis and dis < 300) or cooldown != 0):#dis > teamMateShoot代表會射到隊友
        return -1
    if (action == "NONE" or lives == 0):
        return 0
    return 1



def Shoot(selfX, selfY, gunAngle, targetX, targetY, dis):
    angleGap = abs(getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis))
    angleTan = np.tan(angleGap / 180 * np.pi)

    if (np.cos(angleGap / 180 * np.pi) >= 1 / 2 ** 0.5 and abs(dis * angleTan) < 11 and dis < 300):
        return "SHOOT"
    return "NONE"

def getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis):
    return gunAngle - getTargetAngle(selfX, selfY, targetX, targetY, dis)

def getTargetAngle(selfX, selfY, targetX, targetY, dis):
    target_vec_cos = getXVec(selfX, targetX) / (dis + 1e-7)
    target_vec_sin = getYVec(selfY, targetY) / (dis + 1e-7)

    targetAngle = (np.degrees(np.arctan2(target_vec_sin, target_vec_cos)) + 360) % 360
    return targetAngle
def shootTeamMate(data, selfX, selfY, gunAngle):
    """
    確認這個砲口方向會不會打到隊友
    """
    teamMateShoot = 600
    for tm in data['teammate_info']:
        if (tm['id'] == data['id']):
            continue
        tmX, tmY = tm['x'] + 12.5 + 5 * (tm['angle'] % 90 != 0), tm['y'] + 12.5 + 5 * (tm['angle'] % 90 != 0)
        tmDis = getDistance(selfX, selfY, tmX, tmY)
        if (tmDis != 0 and tm['lives'] > 0):
            if (Shoot(selfX, selfY, gunAngle, tmX, tmY, tmDis) == "SHOOT" and tmDis < teamMateShoot):
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




def enemyReach(graph, data):
    x, y = data['x'] + 12.5 + 5 * int(data['angle'] % 90 == 0), data['y'] + 12.5 + 5 * int(data['angle'] % 90 == 0)
    competitor_info = data['competitor_info']

    enemyFind = []
    for enemy in competitor_info:
        enemy_x, enemy_y = enemy['x'] + 12.5 + 5 * int(enemy['angle'] % 90 == 0), enemy['y'] + 12.5 + 5 * int(enemy['angle'] % 90 == 0)
        if ((seeTarget(x, y, enemy_x, enemy_y, graph) or seeTarget(enemy_x, enemy_y, x, y, graph)) \
            and getDistance(x, y, enemy_x, enemy_y) < 350):
            enemyFind.append(enemy)
    return enemyFind

def seeTarget(x, y, targetX, targetY, graph):
    enemyWayX, enemyWayY = PosNag(targetX - x), PosNag(targetY - y)
    wall_x, wall_y = int(x / 25) + enemyWayX, int(y / 25) + enemyWayY
    targetAngle = getTargetAngle(x, y, targetX, targetY, getDistance(x, y, targetX, targetY))

    


    if (Shoot(x, y, targetAngle, targetX, targetY, 100) == "SHOOT"):#用有沒有瞄準到判斷
        return True

    seeEnemy = True

    if (enemyWayX != 0 and enemyWayY != 0):
        while (wall_x != int(targetX / 25) and wall_x >= 0 and wall_x < 40):
            while (wall_y != int(targetY / 25) and wall_y >= 0 and wall_y < 24):
                if (int(graph[wall_y, wall_x]) > 0):
                    seeEnemy = False
                    break
                wall_y += enemyWayY
            if (not seeEnemy): break
                
            wall_x += enemyWayX
        return seeEnemy

    return False
        

def TurnAngleToEnemy_(selfX, selfY, gunAngle, enemyFind):
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