import numpy as np
import random
def getDistance(x1, y1, x2, y2) -> float:
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
    """
    確認是否瞄準到目標
    """

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
    """
    把奇怪的座標系統變正常
    """

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


#下面應該都是路徑規劃相關?

def findMinResouce(data, name):
    """
    name : oil_stations_info, bullet_stations_info
    """
    x, y, _, _ = getTank(data)

    min_oil_x = 1e4
    min_oil_y = 1e4
    oil_station = []

    atRight = x > 500

    for oil in data[name]:
        if (oil['power'] != 0):
            oil_station.append(oil)

    for o in oil_station:
        oil_x, oil_y = o['x'], o['y']
        if ((atRight and oil_x <= 500) or (not atRight and oil_x > 500)):
            continue
        if (getDistance(x, y, oil_x, oil_y) < getDistance(x, y, min_oil_x, min_oil_y)):
            min_oil_x = oil_x
            min_oil_y = oil_y

    return min_oil_x, min_oil_y

def canGoTarget(x, y, targetX, targetY, graph):
    graphX, graphY = int(x / 25), int(y / 25)
    graphTargetX, graphTargetY = int(targetX / 25), int(targetY / 25)

    xAngle = np.arccos(PosNag(graphTargetX - graphX)) * 180 / np.pi
    yAngle = np.arcsin(-PosNag(graphTargetY - graphY)) * 180 / np.pi

    xDis = abs(graphTargetX - graphX)
    yDis = abs(graphTargetY - graphY)

    #先走x再走y
    if (graphThisAngle(x, y, xAngle, graph) > xDis and graphThisAngle(targetX, y, yAngle, graph) > yDis):
        return 1
    #先走y再走x
    elif (graphThisAngle(x, y, yAngle, graph) > yDis and graphThisAngle(x, targetY, xAngle, graph) > xDis):
        return 2
    else:
        return 0


def getMinDisCP(x, y, checkPointList, graph):
    minDis = 1e9
    minX, minY = 0, 0
    model = 1 #決定先走x方向還是y方向
    for cpX, cpY in checkPointList:
        dis = getDistance(x, y, cpX, cpY)
        avalible = canGoTarget(x, y, cpX, cpY, graph)
        if (dis < minDis and avalible != 0):
            minDis = dis
            minX, minY = cpX, cpY
            model = avalible
    return minX, minY, model

def getTargetCP(x, y, targetX, targetY, checkPointList, graph):
    """
    go target with check point
    """
    minDis = 1e9
    minX, minY = 0, 0
    model = 1 #決定先走x方向還是y方向
    for cpX, cpY in checkPointList:
        dis = getDistance(x, y, cpX, cpY) + getDistance(targetX, targetY, cpX, cpY)
        selfAvalible = canGoTarget(x, y, cpX, cpY, graph)
        targetAvalible = canGoTarget(targetX, targetY, cpX, cpY, graph)
        if (dis < minDis and selfAvalible != 0 and targetAvalible != 0):
            minDis = dis
            minX, minY = cpX, cpY
            model = selfAvalible
    return minX, minY, model



def goTargetDirect(x, y, targetX, targetY, angle, model):
    """
    warning: x, y should be + 12.5 + 5 * int(angle % 90 != 0)

    這必須建立於目標毫無阻礙時
    """
    graphX, graphY = int(x / 25), int(y / 25)
    graphTargetX, graphTargetY = int(targetX / 25), int(targetY / 25)

    xAngle = np.arccos(PosNag(graphTargetX - graphX)) * 180 / np.pi
    yAngle = np.arcsin(-PosNag(graphTargetY - graphY)) * 180 / np.pi
    xDis = abs(graphTargetX - graphX)
    yDis = abs(graphTargetY - graphY)

    if (model == 1): 
        return xFirstWalk(xDis, xAngle, yAngle, angle)
    else:
        return yFirstWalk(yDis, xAngle, yAngle, angle)

def xFirstWalk(xDis, xAngle, yAngle, angle):
    if (xAngle != angle and xDis != 0):
        return turnToAngle(angle, xAngle)
    elif(xDis == 0 and yAngle != angle):
        return turnToAngle(angle, yAngle)
    else:
        return "FORWARD"
def yFirstWalk(yDis, xAngle, yAngle, angle):
    if (yAngle != angle and yDis != 0):
        return turnToAngle(angle, yAngle)
    elif(yDis == 0 and xAngle != angle):
        return turnToAngle(angle, xAngle)
    else:
        return "FORWARD"
def turnToAngle(tankAngle, TargetAngle):
    """
    tankAngle != TargetAngle
    """
    targetAngleGap = (tankAngle - TargetAngle + 360) % 360

    if (targetAngleGap == 0):
        return "FORWARD"
    
    elif (np.sin(targetAngleGap / 180 * np.pi) < 0):
        return "TURN_LEFT"
    else:
        return "TURN_RIGHT"
    

def goTarget(x, y, targetX, targetY, angle, graph, nowCheckPoint):
    model = canGoTarget(x, y, targetX, targetY, graph)
    if (model != 0):
        return goTargetDirect(x, y, targetX, targetY, angle, model)
    else:
        cpX, cpY, model = getTargetCP(x, y, targetX, targetY, nowCheckPoint, graph)

        return goTargetDirect(x, y, cpX, cpY, angle, model)