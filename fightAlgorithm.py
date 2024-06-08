
from fight_train_func import *

def testDataForAgent(dataForAgent):
    Angle, gunAngle, \
    e1x, e1y, e2x, e2y, e3x, e3y, e1Aim, e2Aim, e3Aim, enemyShow1, enemyShow2, enemyShow3 = tuple(dataForAgent)
    
    enemyFind = []

    if (enemyShow1 == 1):
        enemyFind.append({'x' : e1x, 'y' : e1y})
    if (enemyShow2 == 1):
        enemyFind.append({'x' : e2x, 'y' : e2y})
    if (enemyShow3 == 1):
        enemyFind.append({'x' : e3x, 'y' : e3y})

    
    
    if (len(enemyFind) != 0):
        if (int(Angle * 45) != 90):
            if (int(Angle * 45) > 90):
                return "TURN_RIGHT"
            else:
                return "TURN_LEFT"
        if (e1Aim == 1 or e2Aim == 1 or e3Aim == 1):
            
            return random.choice(["FORWARD", "BACKWARD", "SHOOT"])
        
        return TurnAngleToEnemy_(0, 0, gunAngle * 45, enemyFind)

    
    if (int(Angle * 45) != 0):
            if (int(Angle * 45) > 0):
                return "TURN_RIGHT"
            else:
                return "TURN_LEFT"

    
    return random.choice(["FORWARD", "BACKWARD", "TURN_LEFT", "TURN_RIGHT"])

