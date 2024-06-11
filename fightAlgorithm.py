
from fight_train_func import *

def testDataForAgent(dataForAgent):
    Angle, gunAngle, e1Angle, e2Angle, e3Angle, e1Aim, e2Aim, e3Aim, e1Dis, e2Dis, e3Dis = tuple(dataForAgent)
    if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
        return "SHOOT"

    enemyAngle = []
    if (e1Dis <= 1200):
        enemyAngle.append((e1Angle, e1Dis))
    if (e2Dis <= 1200):
        enemyAngle.append((e2Angle, e2Dis))
    if (e3Dis <= 1200):
        enemyAngle.append((e3Angle, e3Dis))

    minDisEnemyAngle, minEnemyDis = GetMinDisEnemy(gunAngle, enemyAngle)
    if (minEnemyDis <= 300):
        return meetEnemy(Angle, gunAngle, minDisEnemyAngle)
    else:
        
        return moveToEnemy(Angle, minDisEnemyAngle)

def testQtableData(QtableData):
    targetAngleDiscrete, AngleDiscrete, gunAngleDiscrete, Aim, minDistanceDiscrete = QtableData

    targetAngle = targetAngleDiscrete * 45
    Angle = AngleDiscrete * 45
    gunAngle = gunAngleDiscrete * 45

    if (Aim == 2):
        return random.choice(["FORWARD", "BACKWARD", "SHOOT"])
    
    if (minDistanceDiscrete == 0):
        return meetEnemy(Angle, gunAngle, targetAngle)

    else:
        return moveToEnemy(Angle, targetAngle)


