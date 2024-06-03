from tank_env.tank_env import tankeEnvBase
from battle import *
import pygame
from playerAlgorithm import player
import random



user_num=6
c = tankeEnvBase(user_num=user_num, green_team_num=int(user_num / 2), blue_team_num=int(user_num / 2), FPS=10, trainMode="map_0_v_0.tmx")
data = c.reset()
if_print = False



move = ["FORWARD", "BACKWARD", "TURN_LEFT", "TURN_RIGHT"]

for i in range(1):
    data = c.reset()

    players = [player(data[str(j) + "P"]) for j in range(1, user_num + 1)]

    while (c.not_done()):
        c.render()
        
        actions = [TurnAngleToTarget(data[str(j) + "P"]) for j in range(1, user_num + 1)]

        
        updateData = {}
        for j in range(1, user_num + 1):
            updateData[str(j) + "P"] = [actions[j - 1]]
            if (actions[j - 1] == "NONE"):
                updateData[str(j) + "P"] = [random.choice(move)]

        data = c.update(updateData)  

        


pygame.quit()

