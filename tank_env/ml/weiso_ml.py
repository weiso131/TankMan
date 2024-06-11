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
from weiso.fight_func import getDataForAgent, getQTableData
from weiso.usefulFunction import *
from weiso.wall_break import  ShootWall, haveWallFourWay




class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = ai_name
        
        self.time = 0
        self.avoidDirect = 0
        self.fightAgent = Q_learning((8, 8, 8, 2, 2, 2), ['AIM_RIGHT', 'AIM_LEFT', 'SHOOT', 'FORWARD', 'BACKWARD', 'TURN_RIGHT', 'TURN_LEFT', 'NONE'])
        self.fightAgent.load(os.path.dirname(os.path.abspath(__file__)) + "/weiso/asset/tank3.pickle")


    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):

        x, y, angle, gunAngle = getTank(scene_info)

        graph = getMapGraph(scene_info)
        
        
        if ((self.avoidDirect == 0 and graphThisAngle(x, y, angle, graph) <= 1) or\
                (self.avoidDirect == 1 and graphThisAngle(x, y, (angle + 180) % 360, graph) <= 1)):
                self.avoidDirect = abs(self.avoidDirect - 1)
        state = getQTableData(getDataForAgent(scene_info, graph, self.avoidDirect))
        # wallRight, wallUp, wallLeft, wallDown = haveWallFourWay(scene_info, x, y, graph)

        # action = ShootWall(gunAngle, wallLeft, wallRight, wallUp, wallDown)

        # if (action == "MEOW"):

        action = self.fightAgent.step(state)

        forwardDis = graphThisAngle(x, y, angle, graph)


             

        return [goToTarget(x, y, 600, 300, graph, angle)]
        

    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")




#python -m mlgame -f 120 -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py . --green_team_num 3 --blue_team_num 3 --frame_limit 1000