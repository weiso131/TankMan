from util import *
import random

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

    return [Angle, gunAngle, wallUp, walldown, wallLeft, wallRight,
             e1x - x, e1y - y, e2x - x, e2y - y, e3x - x, e3y - y, e1Aim, e2Aim, e3Aim, enemyShow[0], enemyShow[1], enemyShow[2]]

def normalizeData(DataForAgent):
    Angle, gunAngle, wallUp, wallDown, wallLeft, wallRight,\
    e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(DataForAgent)

    e1Dis = (e1x ** 2 + e1y ** 2) ** 0.5 + 1e-7
    e2Dis = (e2x ** 2 + e2y ** 2) ** 0.5 + 1e-7
    e3Dis = (e3x ** 2 + e3y ** 2) ** 0.5 + 1e-7

    return Angle / 8, gunAngle / 8, wallUp, wallDown, wallLeft, wallRight,\
    e1x / e1Dis, e1y / e1Dis, e2x / e2Dis, e2y / e2Dis, e3x / e3Dis, e3y / e3Dis, \
        (e1Aim + 1) / 2, (e2Aim + 1) / 2, (e3Aim + 1) / 2, enemyShow1, enemyShow2, enemyShow3


def isAimToYou(selfX, selfY, gunAngle, targetX, targetY, teamMateShootDis):
    dis = getDistance(selfX, selfY, targetX, targetY)
    action = Shoot(selfX, selfY, gunAngle, targetX, targetY, dis)
    if (dis > teamMateShootDis and dis < 300):#dis > teamMateShoot代表會射到隊友
        return -1
    if (action == "NONE"):
        return 0
    return 1


def rewardFunction(DataForAgent, action : str, score, livesLoss):
    reward = livesLoss * (-10) + getScoreReward(score)

    Angle, gunAngle, wallUp, wallDown, wallLeft, wallRight,\
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
        aimAction = TurnAngleToEnemy_(0, 0, gunAngle * 45, enemyFind)
        if (aimAction == action):
            reward += 0.5

    elif (ShootWall(gunAngle * 45, wallLeft, wallRight, wallUp, wallDown) == action):
        reward += 0.001

    return reward




def getScoreReward(score):
    reward = 0
    if (score >= 20):
        reward += int(score / 20) * 10 #打到人10分
        score = score % 20

    if (score >= 5):
        reward += int(score / 5) * 0.01 #打爆牆壁0.02分
        score = score % 5

    return reward + score * 0.01


def Shoot(selfX, selfY, gunAngle, targetX, targetY, dis):
    angleGap = abs(getTargetAngleGap(selfX, selfY, gunAngle, targetX, targetY, dis))
    angleTan = np.tan(angleGap / 180 * np.pi)

    if (np.cos(angleGap / 180 * np.pi) >= 1 / (2 ** 0.5) and abs(dis * angleTan) < 25 and dis < 300):
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