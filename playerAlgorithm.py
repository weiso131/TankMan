import numpy as np
from util import *




class player():

    def __init__(self, initData):
        self.lastX, self.lastY, self.lastMove = initData['x'], initData['y'], "NONE"
        self.turnWay = "NONE"

    def goTarget(self, targetX, targetY, data):
        x = data["x"]
        y = data["y"]
        angleCos, angleSin = getCosSin(data["angle"])
        isStuck = 0

        if (self.lastX == x and self.lastY == y and self.lastMove == "FORWARD"):
            isStuck = 1
        self.lastX = x
        self.lastY = y

        turn = float(1 - int(isStuck)) * (0.99)



        action = "NONE"
        if (self.turnWay != "NONE"):
            action = self.turnWay
            self.turnWay = "NONE"
            return action

        target_vec_x = getXVec(x, targetX) / getDistance(x, y, targetX, targetY)
        target_vec_y = getYVec(y, targetY) / getDistance(x, y, targetX, targetY)
        
        cross = getCross(angleCos, angleSin, target_vec_x, target_vec_y)
        dot = getDot(angleCos, angleSin, target_vec_x, target_vec_y)


        if (dot < 0):
            if (cross > 0):
                action = "TURN_LEFT"
            else:
                action = "TURN_RIGHT"
        else:
            if (abs(cross) <  turn):
                action = "FORWARD"
            elif(cross > turn):
                action =  "TURN_LEFT"
            else:
                action = "TURN_RIGHT"
        if (action != "FORWARD" and action != "NONE"):
            self.turnWay = action
        self.lastMove = action
        return action
    

    def find_oil(self, data):
        x = data["x"]
        y = data["y"]

        min_oil_x = 1e4
        min_oil_y = 1e4
        oil_station = []

        for oil in data["oil_stations_info"]:
            if (oil['power'] != 0):
                oil_station.append(oil)

        if (len(oil_station) == 0):
    
            return "NONE"

        for o in oil_station:
            oil_x, oil_y = o['x'], o['y']
            if (getDistance(x, y, oil_x, oil_y) < getDistance(x, y, min_oil_x, min_oil_y)):
                min_oil_x = oil_x
                min_oil_y = oil_y

        return self.goTarget(min_oil_x, min_oil_y, data)
    


def goTarget(targetX, targetY, data):
        x = data["x"]
        y = data["y"]
        angleCos, angleSin = getCosSin(data["angle"])
        isStuck = 0

        

        turn = float(1 - int(isStuck)) * (0.99)



        action = "NONE"


        target_vec_x = getXVec(x, targetX) / getDistance(x, y, targetX, targetY)
        target_vec_y = getYVec(y, targetY) / getDistance(x, y, targetX, targetY)
        
        cross = getCross(angleCos, angleSin, target_vec_x, target_vec_y)
        dot = getDot(angleCos, angleSin, target_vec_x, target_vec_y)


        if (dot < 0):
            if (cross > 0):
                action = "TURN_LEFT"
            else:
                action = "TURN_RIGHT"
        else:
            if (abs(cross) <  turn):
                action = "FORWARD"
            elif(cross > turn):
                action =  "TURN_LEFT"
            else:
                action = "TURN_RIGHT"
        return action