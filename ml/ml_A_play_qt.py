"""
The template of the main script of the machine learning process
"""
import pygame
import os
import sys
import pickle
from datetime import datetime
import numpy as np
import pandas as pd
import math
sys.path.append(os.path.dirname(__file__))
from env import *
from ml_A_Environment import Environment as env
from QT import QLearningTable


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
        

        self.QT = QLearningTable(actions=list(range(self.env.n_actions)), e_greedy=0)
        
        folder_path = os.path.dirname(__file__) + '/save'                              
        self.QT.q_table = pd.read_pickle(folder_path+'/A_qtable.pickle')
        

        self.action_mapping = [["NONE"], ["TURN_LEFT"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"]]
         

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        
        
        if scene_info["status"] != "GAME_ALIVE":            
            return "RESET"
        
        self.env.set_scene_info(scene_info)        
        observation, reward, done, info = self.env.step(self.action)


        self.state = [observation]
        action = self.QT.choose_action(str(self.state))        

        
        self.action = action           
        command = self.action_mapping[action]
              
        return command


    def reset(self):
        """
        Reset the status
        """
        print(f"reset Game {self.side}")
        
    
    