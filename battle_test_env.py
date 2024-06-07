from tank_env.tank_env import tankeEnvBase
from battle import *
import pygame
from playerAlgorithm import *
import random
from util import *
import numpy as np

user_num=6
c = tankeEnvBase(user_num=user_num, green_team_num=int(user_num / 2), blue_team_num=int(user_num / 2), FPS=30, trainMode="attack_train.tmx")#map_0_v_0.tmx
data = c.reset()
if_print = False




move = ["FORWARD", "BACKWARD", "TURN_LEFT", "TURN_RIGHT"]

for i in range(1):
    data = c.reset()

    players = [player(data[str(j) + "P"]) for j in range(1, user_num + 1)]
     
    
    while (c.not_done()):
        c.render()
        
        graph = getMapGraph(data['1P'])

        updateData = {}
        for j in range(1, user_num + 1):
            playerID = str(j) + "P"
            action = shootWall(graph, data[playerID])
            updateData[playerID] = [action]
            
        
        
        data = c.update(updateData)  

        


pygame.quit()

