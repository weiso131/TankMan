from tank_env.tank_env import tankeEnvBase
from battle import *
import pygame
from playerAlgorithm import *
from util import *
from attack_train_func import *
from battleAlgorithm import testDataForAgent

user_num=6
c = tankeEnvBase(user_num=user_num, green_team_num=int(user_num / 2), blue_team_num=int(user_num / 2), FPS=60, trainMode="attack_train_wall.tmx")#map_0_v_0.tmx
data = c.reset()
if_print = False




move = ["FORWARD", "BACKWARD", "TURN_LEFT", "TURN_RIGHT"]

for i in range(1):
    data = c.reset()

    players = [player(data[str(j) + "P"]) for j in range(1, user_num + 1)]
    lives = [0, 3, 3, 3, 3, 3, 3]
    scores = [0, 0, 0, 0, 0, 0, 0]
    
    while (c.not_done()):
        c.render()
        
        graph = getMapGraph(data['1P'])
        updateData = {}
        for j in range(1, user_num + 1):
            playerID = str(j) + "P"

            scoreUp = data[playerID]['score'] - scores[j]
            liveLoss = data[playerID]['lives'] - lives[j]
            scores[j] = data[playerID]['score']
            lives[j] = data[playerID]['lives']

            DataForAgent = getDataForAgent(data[playerID], graph)
            action = testDataForAgent(DataForAgent)
            reward = rewardFunction(DataForAgent, action, scoreUp, liveLoss)

            
            updateData[playerID] = [action]
            print(DataForAgent, reward)
        data = c.update(updateData)  

        


pygame.quit()

