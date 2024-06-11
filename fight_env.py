

from tank_env.tank_env import tankeEnvBase
from fight_train_func import getDataForAgent, PosNag, graphThisAngle

import numpy as np
class fight_env(tankeEnvBase):

    def __init__(self, user_num=6, green_team_num=3, blue_team_num=3, FPS=60, trainMode="plain.tmx"):
        super().__init__(user_num, green_team_num, blue_team_num, FPS, trainMode)
        self.bullet_info = {'1P_bullet' : (-1, -1, -1, -1),
                            '2P_bullet' : (-1, -1, -1, -1),
                            '3P_bullet' : (-1, -1, -1, -1),
                            '4P_bullet' : (-1, -1, -1, -1),
                            '5P_bullet' : (-1, -1, -1, -1),
                            '6P_bullet' : (-1, -1, -1, -1),}
        
        self.avoidDirect = [0, 0, 0, 0, 0, 0, 0]
        
    
    def getDataForAllAgent(self)->dict:

        data = self.game.get_data_from_game_to_player()

        

        DataForAgents = {}#state, lives, scores
        graph = self.getMapGraph(data['1P'])
        self.getBullet(data['1P'], graph)
        for i in range(1, 7):
            playerID = str(i) + "P"
            x, y, tankeAngle, _ = getTank(data[playerID])

            if ((self.avoidDirect[i] == 0 and graphThisAngle(x, y, tankeAngle, graph) <= 1) or\
                (self.avoidDirect[i] == 1 and graphThisAngle(x, y, (tankeAngle + 180) % 360, graph) <= 1)):
                self.avoidDirect[i] = abs(self.avoidDirect[i] - 1)


            
            DataForAgents[playerID] = (getDataForAgent(data[playerID], graph, self.avoidDirect[i]), 
                                       data[playerID]['lives'] - self.lives[i], 
                                       data[playerID]['score'] - self.scores[i])
            self.scores[i] = data[playerID]['score']
            self.lives[i] = data[playerID]['lives']

        return DataForAgents
    

    def getBullet(self, data, graph):
        bullet_info = data["bullets_info"]

        existBullet = []

        for b in bullet_info:
            id = b["id"]
            startX, startY = b['x'], b['y']
            existBullet.append(id)
            if (self.bullet_info[id][0] == -1):
                
                angle = (b['rot'] + 540 ) %  360
                cos, sin = PosNag(np.cos(angle / 180 * np.pi)), PosNag(np.sin(angle / 180 * np.pi))

                if (angle % 90 == 0):
                    self.bullet_info[id] = (startX, startY, startX + 300 * cos, startY - 300 * sin)
                else:
                    self.bullet_info[id] = (startX, startY, startX + 210 * cos, startY - 210 * sin)


        for i in range(1, 7):
            key = str(i) + 'P_bullet'
            if (not (key in existBullet)):
                self.bullet_info[key] = (-1, -1, -1, -1)
        


def getTank(data):
    Angle = (data['angle'] + 540) % 360
    return data['x'] + 12.5 + 5 * int(Angle % 90 != 0), data['y'] + 12.5 + 5 * int(Angle % 90 != 0), Angle, (data['gun_angle'] + 540) % 360