"""
The template of the main script of the machine learning process
"""
import pygame
import os
import pickle
from datetime import datetime
import numpy as np
from ml.Environment import Environment as env
from ml.QT import QLearningTable
import pandas as pd
import math
from ml.env import *


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """        
        self.side = ai_name
        print(f"Initial Game {ai_name} ml script")
        self.time = 0

        self.env = env()
        self.action = self.env.action
        self.state = [self.env.observation]    
        self.state_ = [self.env.observation]         

        self.QT = QLearningTable(actions=list(range(self.env.n_actions)))
        
        folder_path = './ml/save'
        os.makedirs(folder_path, exist_ok=True)

        
        self.QT.q_table =pd.read_pickle('.\\ml\\save\\qtable.pickle')
        

        self.action_mapping = [["NONE"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"]]            
         

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        
        
        if scene_info["status"] != "GAME_ALIVE":            
            return "RESET"
        
        self.env.set_scene_info(scene_info)        
        observation, reward, done, info = self.env.step(self.action)


        self.state_ = [observation]
        action = self.QT.choose_action(str(self.state))
        


        self.state = self.state_
        self.action = action           
        command = self.action_mapping[action]

        is_wall_in_bullet_range = self.is_wall_in_bullet_range({"x": scene_info["x"], "y": scene_info["y"]}, scene_info["gun_angle"], scene_info["walls_info"], 50)
        
        is_target_in_bullet_range = self.is_target_in_bullet_range({"x": scene_info["x"], "y": scene_info["y"]}, scene_info["gun_angle"], {"x":scene_info["competitor_info"][0]["x"], "y":scene_info["competitor_info"][0]["y"]}, BULLET_TRAVEL_DISTANCE)
        if is_wall_in_bullet_range or is_target_in_bullet_range:
            command = ["SHOOT"]
        return command


    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
        self.QT.q_table.to_pickle('.\\ml\\save\\qtable.pickle')

    def is_wall_in_bullet_range(self, tank_pos, gun_angle, walls, detection_distance):
        for wall in walls:            
            if self.will_hit_target(tank_pos, gun_angle, {"x":wall["x"], "y":wall["y"]}, detection_distance):
                return True    
        return False

    def is_target_in_bullet_range(self, tank_pos, gun_angle, target_pos, detection_distance):
        return self.will_hit_target(tank_pos, gun_angle, target_pos, detection_distance)

    def will_hit_target(self, tank_pos, gun_angle, target_pos, detection_distance):    
        distance = math.sqrt((tank_pos["x"] - target_pos["x"]) ** 2 + (tank_pos["y"] - target_pos["y"]) **2)
        
        if detection_distance < distance:
            return False
        
        angle_rad = math.atan2(target_pos["y"] - tank_pos["y"], target_pos["x"] - tank_pos["x"])            
        gun_rad = np.radians(180 - gun_angle) 
        toarance_rad = math.atan2(WALL_WIDTH/2, distance)
        
        
        return abs(gun_rad - angle_rad) < toarance_rad   
    