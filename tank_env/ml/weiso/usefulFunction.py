import numpy as np

def getDistance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def getCross(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1
def getDot(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def getYVec(y, targetY):
    return y - targetY
def getXVec(x, targetX):
    return targetX - x

def getCosSin(angle):
    """
    角度加180
    """
    angleCos = np.cos((angle + 180) / 180 * np.pi)
    angleSin = np.sin((angle + 180) / 180 * np.pi)

    return angleCos, angleSin
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
def getMapGraph(data):
    MapGraph = np.zeros((24, 40))
    for wall in data['walls_info']:
        wallX = int(wall['x'] / 25)
        wallY = int(wall['y'] / 25)
        MapGraph[wallY, wallX] = 1
        
    return MapGraph
def shootTeamMate(data, selfX, selfY, gunAngle):
    """
    確認這個砲口方向會不會打到隊友
    """
    teamMateShoot = 600
    for tm in data['teammate_info']:
        if (tm['id'] == data['id']):
            continue
        tmDis = getDistance(selfX, selfY, tm['x'], tm['y'])
        if (tmDis != 0 and tm['lives'] > 0):
            if (Shoot(selfX, selfY, gunAngle, tm['x'], tm['y'], tmDis) == "SHOOT" and tmDis < teamMateShoot):
                print(data['id'], tm['id'])
                teamMateShoot = tmDis  
    return teamMateShoot
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

def getTank(data):
    Angle = (data['angle'] + 540) % 360
    return data['x'] + 12.5 + 5 * (Angle % 90 != 0), data['y'] + 12.5 + 5 * (Angle % 90 != 0), (Angle + 540) % 360, (data['gun_angle'] + 540) % 360


def graphThisAngle(x, y, angle, graph):
    """
    angle : 0, 45, 90, ...

    value : -1邊界

    value : 1 牆壁

    value : 2 隊友

    return: 走幾步碰到某個值, 該值
    """
    cos, sin = PosNag(cos(angle)), PosNag(sin(angle))

    graphX, graphY = int(x / 25), int(y / 25)

    takeLeft = (-sin, -cos)
    takeRight = (sin, cos)
    if (angle % 90 == 0):
        takeLeft = (0, -1)
        takeRight = (-1, 0)

    step = 1
    value = -1
    while (step * cos + graphX):
        step += 1
    
    
        



    return step, value