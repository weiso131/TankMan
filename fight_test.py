from fight_env import fight_env

import pygame

from fight_train_func import *
from fightAlgorithm import testDataForAgent


c = fight_env()#map_0_v_0.tmx


for i in range(1):
    data = c.reset()

   
    lives = [0, 3, 3, 3, 3, 3, 3]
    scores = [0, 0, 0, 0, 0, 0, 0]
    
    while (c.not_done()):
        c.render()
        
        
        updateData = {}
        oldState = {}
        actions = {}
        for j in range(1, 7):
            playerID = str(j) + "P"

            state, _, _ = data[playerID]
            oldState[playerID] = state
            action = testDataForAgent(state)
            updateData[playerID] = [action]
            actions[playerID] = action
        data = c.update(updateData)  

        for j in range(1, 7):
            playerID = str(j) + "P"
            new_state, liveLoss, scoreUp = data[playerID]

            reward = rewardFunction(oldState[playerID], \
                                    actions[playerID], scoreUp, liveLoss)
            
            done = int(c.lives[j] == 0)

            if (j == 1 and reward != 0):
                print(len(normalizeData(oldState[playerID])))
                print(f"old_state:{normalizeData(oldState[playerID])}\nnew_state:{normalizeData(new_state)}\naction:{actions[playerID]}, reward:{reward}, done: {done}")


pygame.quit()

