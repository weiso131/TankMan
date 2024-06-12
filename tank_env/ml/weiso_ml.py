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
from weiso.fight_func import getDataForAgent, getQTableData, seeEnemy, getBullet, avoidBullet, enemySameSide
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
        otherCheckPoint = self.leftCheckPoint
        self.bullet_history, graph = getBullet(scene_info, self.bullet_history, graph)
        enemyTarget = enemySameSide(scene_info)
        

        if (x < 500):
            nowCheckPoint = self.leftCheckPoint
            otherCheckPoint = self.rightCheckPoint
            front = 425
        if ((int(scene_info['id'][0]) > 3 and x >= 500) or (int(scene_info['id'][0]) <= 3 and x < 500)):
            haveBreakWall = True
            
        if ((self.avoidDirect == 0 and graphThisAngle(x, y, angle, graph) <= 1) or (self.avoidDirect == 1 and graphThisAngle(x, y, (angle + 180) % 360, graph) <= 1)):
            self.avoidDirect = abs(self.avoidDirect - 1)
        wallAngle = 0
        if (int(scene_info['id'][0]) < 4):
            wallAngle = 180 #只打隔絕一切的城牆

        shootWall = getShootWallAgree(x, y, wallAngle, scene_info, graph)

        action = "NONE"
        
        #被子彈彈道瞄準到
        if (graph[int(y / 25), int(x / 25)] < 0):
            action = avoidBullet(graph[int(y / 25), int(x / 25)], angle, self.bullet_history, self.avoidDirect)

        #缺油撿油
        elif (scene_info['oil'] < 30):
            oil_x, oil_y = findMinResouce(scene_info, "oil_stations_info")
            action = goTarget(x, y, oil_x, oil_y, angle, graph, nowCheckPoint)
        
        #缺子彈撿子彈
        elif (scene_info['power'] == 0):
            
            bullet_x, bullet_y = findMinResouce(scene_info, "bullet_stations_info")
            action = goTarget(x, y, bullet_x, bullet_y, angle, graph, nowCheckPoint)
            print(scene_info['id'], action, end=" ")
        
        #判斷是否進入戰鬥模式
        elif (seeEnemy(scene_info, graph) and scene_info["oil"] > 50 and scene_info["power"] != 0):
            state = getQTableData(getDataForAgent(scene_info, graph, self.avoidDirect))
            
            action = self.fightAgent.step(state)

        #敵人跟自己同一邊的時候，追他
        elif (enemyTarget[0] != -1000 and scene_info["power"] != 0):
            action = goTarget(x, y, enemyTarget[0], enemyTarget[1], angle, graph, nowCheckPoint)

        #還沒攻進對面陣地的時候，衝到前線炸牆壁
        elif (abs(x - 500) > 100 and not haveBreakWall and scene_info["power"] != 0):
            action = goTarget(x, y, front, y, angle, graph, nowCheckPoint)

        if (action == "NONE"):
            enemySurvive = 0
            otherSideAction = goOtherSide(x, y, angle, graph, nowCheckPoint, otherCheckPoint)
            for enemy in scene_info["competitor_info"]:
                if (enemy["lives"] > 0): enemySurvive += 1

            if (enemySurvive == 1 and otherSideAction != "NONE" and scene_info["power"] != 0):
                action = otherSideAction
            elif (shootWall and scene_info['power'] != 0 and scene_info['oil'] > 30):#打牆壁
                action = turnGunToWall(gunAngle, wallAngle)
            elif (angle % 180 != 90):
                action = "TURN_RIGHT"
            elif(self.avoidDirect == 0):
                action = "FORWARD"
            else:
                action = "BACKWARD"
        

        

        
        return [action]
            
    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
    

        #print(self.bullet_info)



#python -m mlgame -f 120 -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py -i ml/weiso_ml.py . --green_team_num 3 --blue_team_num 3 --frame_limit 1000