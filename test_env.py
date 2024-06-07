from tank_env.tank_env import tankeEnvBase
from battle import *
import pygame
from playerAlgorithm import *
import random
import numpy as np


user_num=6
c = tankeEnvBase(user_num=user_num, green_team_num=int(user_num / 2), blue_team_num=int(user_num / 2), FPS=30, trainMode="map_3_v_3 copy.tmx")
data = c.reset()
if_print = False



move = ["FORWARD", "BACKWARD", "TURN_LEFT", "TURN_RIGHT"]




for i in range(1):
    data = c.reset()

    players = [player(data[str(j) + "P"]) for j in range(1, user_num + 1)]

    while (c.not_done()):
        c.render()
        
        Map = getMapGraph(data['1P'])



        actions = []


        for j in range(1, user_num + 1):
            if (players[j - 1].pointQueue.empty()):
                players[j - 1].find_oil(data[str(j) + 'P'], Map)
            actions.append(players[j - 1].goTarget(data[str(j) + 'P']))

        
        updateData = {}
        for j in range(1, user_num + 1):
            updateData[str(j) + "P"] = [actions[j - 1]]

        data = c.update(updateData)  

        


pygame.quit()

