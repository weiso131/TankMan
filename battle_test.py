from train_attack_model_env import attack_env
from battle import *
import pygame
from playerAlgorithm import *
from util import *
from attack_train_func import *
from battleAlgorithm import testDataForAgent

user_num=6
c = attack_env(user_num=user_num, green_team_num=int(user_num / 2), blue_team_num=int(user_num / 2), FPS=60, trainMode="plain.tmx")#map_0_v_0.tmx


for i in range(1):
    data = c.reset()

   
    lives = [0, 3, 3, 3, 3, 3, 3]
    scores = [0, 0, 0, 0, 0, 0, 0]
    
    while (c.not_done()):
        c.render()
        
        
        updateData = {}
        oldState = {}
        actions = {}
        for j in range(1, user_num + 1):
            playerID = str(j) + "P"

            state, _, _ = data[playerID]
            oldState[playerID] = state
            action = testDataForAgent(state)
            updateData[playerID] = [action]
            actions[playerID] = action
        data = c.update(updateData)  

        for j in range(1, user_num + 1):
            playerID = str(j) + "P"
            new_state, liveLoss, scoreUp = data[playerID]

            reward = rewardFunction(oldState[playerID], \
                                    actions[playerID], scoreUp, liveLoss)
            
            done = int(c.lives[j] == 0)

            if (j == 1 and reward != 0):
                print(len(oldState[playerID]))
                print(f"old_state:{normalizeData(oldState[playerID])}\nnew_state:{normalizeData(new_state)}\naction:{actions[playerID]}, reward:{reward}, done: {done}")


pygame.quit()

