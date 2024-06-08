

from tank_env.tank_env import tankeEnvBase
from fight_train_func import getDataForAgent


class fight_env(tankeEnvBase):

    def __init__(self, user_num=6, green_team_num=3, blue_team_num=3, FPS=60, trainMode="plain.tmx"):
        super().__init__(user_num, green_team_num, blue_team_num, FPS, trainMode)
        
        
    
    def getDataForAllAgent(self)->dict:

        data = self.game.get_data_from_game_to_player()

        DataForAgents = {}#state, lives, scores
        graph = self.getMapGraph(data['1P'])
        for i in range(1, 7):
            playerID = str(i) + "P"
            DataForAgents[playerID] = (getDataForAgent(data[playerID], graph), 
                                       data[playerID]['lives'] - self.lives[i], 
                                       data[playerID]['score'] - self.scores[i])
            self.scores[i] = data[playerID]['score']
            self.lives[i] = data[playerID]['lives']

        return DataForAgents




    