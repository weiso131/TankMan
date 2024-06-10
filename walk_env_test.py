from tank_env.tank_env import tankeEnvBase

from playerAlgorithm import *
from attack_train_func import PosNag

import pygame

import random


env = tankeEnvBase()#map_0_v_0.tmx



def canWalkToXLine(x : int, y : int, lineX : int, graph):
    wayX = PosNag(lineX - x)
    if (wayX != 0):
        for i in range(x + wayX, lineX + wayX, wayX):
            if (graph[y, i] != 0):
                return False
    return True
def canWalkToYLine(x : int, y : int, lineY : int, graph):
    wayY = PosNag(lineY - y)
    if (wayY != 0):

        for i in range(y + wayY, lineY + wayY, wayY):
            if (graph[i, x] != 0):
                return False
    return True

def walkDirection(x, y, targetX, targetY, graph):
    graph_x, graph_y = int(x / 25), int(y / 25)
    graphTargetX, graphTargetY = int(targetX / 25), int(targetY / 25)

    if (graph_x == graphTargetX):
        if (canWalkToYLine(graph_x, graph_y, graphTargetY, graph)):
            pass


for i in range(1):
    data = env.reset()

    while (env.not_done()):
        env.render()
        graph = env.getMapGraph(data['1P'])
        
        updateData = {}
        for j in range(1, 7):
            playerID = str(j) + "P"
            angle = data[playerID]['angle']
            x, y = data[playerID]['x'] + 12.5 + 5 * int(angle % 90 == 0), data[playerID]['y'] + 12.5 + 5 * int(angle % 90 == 0)
            
            oil_x, oil_y = find_oil(data[playerID])
            print(data[playerID]['id'], canWalkToXLine(int(x / 25), int(y / 25), int(600 / 25), graph), "x")
            print(data[playerID]['id'], canWalkToYLine(int(x / 25), int(y / 25), int(300 / 25), graph), "y")
            updateData[playerID] = ["NONE"]
            


        data = env.update(updateData)
            


pygame.quit()


