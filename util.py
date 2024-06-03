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