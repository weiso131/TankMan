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
from weiso.usefulFunction import getMapGraph, getTank, graphThisAngle
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

        self.fightAgent = Q_learning((8, 8, 8, 3, 2), ['AIM_RIGHT', 'AIM_LEFT', 'SHOOT', 'FORWARD', 'BACKWARD', 'TURN_RIGHT', 'TURN_LEFT', 'NONE'])
        self.fightAgent.load(os.path.dirname(os.path.abspath(__file__)) + "/weiso/asset/tank2.pickle")


    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):

        x, y, angle, gunAngle = getTank(scene_info)

        graph = getMapGraph(scene_info)
        
        state = getQTableData(getDataForAgent(scene_info, graph))
        

        wallRight, wallUp, wallLeft, wallDown = haveWallFourWay(scene_info, x, y, graph)

        action = ShootWall(gunAngle, wallLeft, wallRight, wallUp, wallDown)

        if (action == "MEOW"):

            action = self.fightAgent.step(state)

        forwardDis = graphThisAngle(x, y, angle, graph)

        if (forwardDis > 1):
            return ["FORWARD"]
        else:
            return ["TURN_RIGHT"]

        return ["NONE"]
        

    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")