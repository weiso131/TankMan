"""
The template of the main script of the machine learning process
"""
import random
import pygame

from src.env import IS_DEBUG

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weiso.Q_learing import Q_learning
from weiso.fight_func import getDataForAgent, getQTableData, seeEnemy
from weiso.usefulFunction import *
from weiso.wall_break import  turnGunToWall, haveWall




class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.side = ai_name
        
        self.time = 0
        self.avoidDirect = 0
        self.fightAgent = Q_learning((8, 8, 8, 2, 2, 2), ['AIM_RIGHT', 'AIM_LEFT', 'SHOOT', 'FORWARD', 'BACKWARD', 'TURN_RIGHT', 'TURN_LEFT', 'NONE'])
        self.fightAgent.load(os.path.dirname(os.path.abspath(__file__)) + "/weiso/asset/tank3.pickle")

        self.leftCheckPoint = []
        self.rightCheckPoint = []
        self.middleCheckPoint = []


    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):

        x, y, angle, gunAngle = getTank(scene_info)

        graph = getMapGraph(scene_info)

        #判斷是否進入戰鬥模式
        if (seeEnemy(scene_info, graph) and scene_info["oil"] > 50 and scene_info["power"] > 0):
            
            print(scene_info['id'], "參上")

            if ((self.avoidDirect == 0 and graphThisAngle(x, y, angle, graph) <= 1) or\
                (self.avoidDirect == 1 and graphThisAngle(x, y, (angle + 180) % 360, graph) <= 1)):
                self.avoidDirect = abs(self.avoidDirect - 1)
            state = getQTableData(getDataForAgent(scene_info, graph, self.avoidDirect))
            
            action = self.fightAgent.step(state)


            return [action]

        #判斷是否打牆
        wallAngle = 0
        if (x >= 500):
            wallAngle = 180 #只打隔絕的牆

        shootWall = haveWall(graph, int(x / 25), int(y / 25), wallAngle) <= 300

        if (shootWall and abs(x - 500) < 100 and scene_info['power'] > 0 and scene_info['oil'] > 50):
            return [turnGunToWall(gunAngle, wallAngle)]
       


        if (graphThisAngle(x, y, angle, graph) > 1):
             return ["FORWARD"]
        else:
             return ["TURN_RIGHT"]
        
        
        
        

    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")




#python -m mlgame -f 120 -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py . --green_team_num 3 --blue_team_num 3 --frame_limit 1000