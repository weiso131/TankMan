from tank_env.tank_env import tankeEnvBase
from attack_train_func import rewardFunction, getDataForAgent

import numpy as np

def getMapGraph(data):
    MapGraph = np.zeros((24, 40))
    for wall in data['walls_info']:
        wallX = int(wall['x'] / 25)
        wallY = int(wall['y'] / 25)
        MapGraph[wallY, wallX] = 1
        
    return MapGraph

class attack_env(tankeEnvBase):

    def __init__(self, user_num=6, green_team_num=3, blue_team_num=3, FPS=60, trainMode="attack_train_wall.tmx"):
        super().__init__(user_num, green_team_num, blue_team_num, FPS, trainMode)
        self.actionSpace = ["AIM_RIGHT", "AIM_LEFT", "SHOOT", "FORWARD", "BACKWARD", "TURN_RIGHT", "TURN_LEFT", "NONE"]
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.lives = [0, 3, 3, 3, 3, 3, 3]
        

    def update(self, actions: dict):
        self.game.update(actions)

        return self.getDataForAllAgent()


    def reset(self):
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.lives = [0, 3, 3, 3, 3, 3, 3]

        self.game.reset()

        return self.getDataForAllAgent()
    
    def getDataForAllAgent(self)->dict:

        data = self.game.get_data_from_game_to_player()

        DataForAgents = {}#state, lives, scores
        graph = getMapGraph(data['1P'])
        for i in range(1, 7):
            playerID = str(i) + "P"
            DataForAgents[playerID] = (getDataForAgent(data[playerID], graph), 
                                       data[playerID]['lives'] - self.lives[i], 
                                       data[playerID]['score'] - self.scores[i])
            self.scores[i] = data[playerID]['score']
            self.lives[i] = data[playerID]['lives']

        return DataForAgents




    