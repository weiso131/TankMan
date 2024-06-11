import numpy as np
import random 
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
        tmX, tmY = tm['x'] + 12.5 + 5 * (tm['angle'] % 90 != 0), tm['y'] + 12.5 + 5 * (tm['angle'] % 90 != 0)
        tmDis = getDistance(selfX, selfY, tmX, tmY)
        if (tmDis != 0 and tm['lives'] > 0):
            if (Shoot(selfX, selfY, gunAngle, tmX, tmY, tmDis) == "SHOOT" and tmDis < teamMateShoot):
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
    return data['x'] + 12.5 - 5 * int(Angle % 90 != 0), data['y'] + 12.5 - 5 * int(Angle % 90 != 0), Angle, (data['gun_angle'] + 540) % 360


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


def goToTarget(x, y, targetX, targetY, graph, angle):
    """
    warning: x, y should be + 12.5 + 5 * int(angle % 90 != 0)
    """
    graphX, graphY = int(x / 25), int(y / 25)
    graphTargetX, graphTargetY = int(targetX / 25), int(targetY / 25)

    xAngle = np.arccos(PosNag(graphTargetX - graphX)) * 180 / np.pi
    yAngle = np.arcsin(-PosNag(graphTargetY - graphY)) * 180 / np.pi

    

    xDis = abs(graphTargetX - graphX)
    yDis = abs(graphTargetY - graphY)
    if (xDis <= graphThisAngle(x, y, xAngle, graph) - 1 and xDis != 0):
        print(x, y)
        return turnToAngle(angle, xAngle)
    elif (yDis <= graphThisAngle(x, y, yAngle, graph) - 1 and yDis != 0):
        print(x, y)
        return turnToAngle(angle, yAngle)
    elif (xDis == 0 and yDis == 0):
        return "SHOOT"
    else:
        return "NONE"

def turnToAngle(tankAngle, TargetAngle):
    
    targetAngleGap = (tankAngle - TargetAngle + 360) % 360

    if (targetAngleGap == 0):
        return "FORWARD"
    
    elif (np.sin(targetAngleGap / 180 * np.pi) < 0):
        return "TURN_LEFT"
    else:
        return "TURN_RIGHT"
    
    
    