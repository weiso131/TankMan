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
from weiso.fight_func import getDataForAgent, getQTableData, seeEnemy, getBullet, avoidBullet
from weiso.usefulFunction import *
from weiso.wall_break import  turnGunToWall, getShootWallAgree




class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.side = ai_name
        
        self.time = 0
        self.avoidDirect = 0
        self.fightAgent = Q_learning((8, 8, 8, 2, 2, 2), ['AIM_RIGHT', 'AIM_LEFT', 'SHOOT', 'FORWARD', 'BACKWARD', 'TURN_RIGHT', 'TURN_LEFT'])
        self.fightAgent.load(os.path.dirname(os.path.abspath(__file__)) + "/weiso/asset/UNDERTAKER.pickle")

        self.leftCheckPoint = [(425, 50), (50, 50), (425, 225), (50, 225), (425, 525), (50, 525)]
        self.rightCheckPoint = [(575, 50), (925, 50), (575, 225), (925, 225), (575, 525), (925, 525)]

        self.middleCheckPoint = []

        
        self.bullet_history = {'1P_bullet' : (-1, -1, -1, -1, -1),
                            '2P_bullet' : (-1, -1, -1, -1, -1),
                            '3P_bullet' : (-1, -1, -1, -1, -1),
                            '4P_bullet' : (-1, -1, -1, -1, -1),
                            '5P_bullet' : (-1, -1, -1, -1, -1),
                            '6P_bullet' : (-1, -1, -1, -1, -1),}#startx, y, endx, y, rot

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        haveBreakWall = False
        x, y, angle, gunAngle = getTank(scene_info)
        graph = getMapGraph(scene_info)
        front = 575
        nowCheckPoint = self.rightCheckPoint
        self.bullet_history, graph = getBullet(scene_info, self.bullet_history, graph)

        

        if (x < 500):
            nowCheckPoint = self.leftCheckPoint
            front = 425
        if ((int(scene_info['id'][0]) > 3 and x >= 500) or (int(scene_info['id'][0]) <= 3 and x < 500)):
            haveBreakWall = True
            
        if ((self.avoidDirect == 0 and graphThisAngle(x, y, angle, graph) <= 1) or (self.avoidDirect == 1 and graphThisAngle(x, y, (angle + 180) % 360, graph) <= 1)):
            self.avoidDirect = abs(self.avoidDirect - 1)
        wallAngle = 0
        if (int(scene_info['id'][0]) < 4):
            wallAngle = 180 #只打隔絕一切的城牆

        shootWall = getShootWallAgree(x, y, wallAngle, scene_info, graph)

        action = "MEOW"
        
        if (graph[int(y / 25), int(x / 25)] < 0):#被子彈彈道瞄準到
            action = avoidBullet(graph[int(y / 25), int(x / 25)], angle, self.bullet_history, self.avoidDirect)

        elif (scene_info['oil'] < 50):
            oil_x, oil_y = findMinResouce(scene_info, "oil_stations_info")
            action = goTarget(x, y, oil_x, oil_y, angle, graph, nowCheckPoint)
        
        elif (scene_info['power'] == 0):
            bullet_x, bullet_y = findMinResouce(scene_info, "bullet_stations_info")
            action = goTarget(x, y, bullet_x, bullet_y, angle, graph, nowCheckPoint)

        #判斷是否進入戰鬥模式
        elif (seeEnemy(scene_info, graph) and scene_info["oil"] > 50 and scene_info["power"] != 0):
            print(scene_info["id"], "戰鬥模式啟動")
            state = getQTableData(getDataForAgent(scene_info, graph, self.avoidDirect))
            
            action = self.fightAgent.step(state)

        elif (shootWall and abs(x - 500) < 100 and scene_info['power'] > 0 and scene_info['oil'] > 50):
            action = turnGunToWall(gunAngle, wallAngle)
               
        #還沒攻進對面陣地的時候，衝到前線炸牆壁
        elif (abs(x - 500) > 100 and not haveBreakWall):
            action = goTarget(x, y, front, y, angle, graph, nowCheckPoint)

        elif (abs(x - 500) <= 100 and not haveBreakWall):
            if (angle % 180 != 90):
                action = "TURN_RIGHT"
            elif(self.avoidDirect == 0):
                action = "FORWARD"
            else:
                action = "BACKWARD"
        if (action == "NONE"):
            print(scene_info['id'], "NONE")
        if (action == "MEOW"):
            print(scene_info['id'], "MEOW", abs(x - 500), haveBreakWall)
        
        #攻進對面陣地的時候，追著人打(待實現)

        
        return [action]
            
    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
    

        #print(self.bullet_info)



#python -m mlgame -f 120 -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py . --green_team_num 3 --blue_team_num 3 --frame_limit 1000