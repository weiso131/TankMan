import pygame
from mlgame.game.generic import quit_or_esc
from mlgame.view.view import PygameView

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.Game import Game
import numpy as np

class tankeEnvBase():
    
    def __init__(self, user_num=6, green_team_num=3, blue_team_num=3, FPS=60, trainMode="normal"):

        # initialize game
        self.frame = 1000
        self.sound = "off"
        self.is_manual = False
        self.FPS = FPS
        self.user_num = user_num
        self.green_team_num = green_team_num
        self.blue_team_num = blue_team_num

        self.game = Game(self.user_num, self.green_team_num, 
                    self.blue_team_num, self.is_manual, self.frame, self.sound, trainMode=trainMode)

        self.actionSpace = ["AIM_RIGHT", "AIM_LEFT", "SHOOT", "FORWARD", "BACKWARD", "TURN_RIGHT", "TURN_LEFT", "NONE"]
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.lives = [0, 3, 3, 3, 3, 3, 3]

            
    
    def update(self, actions: dict):
        self.game.update(actions)

        return self.getDataForAllAgent()

    def render(self):
        pygame.time.Clock().tick_busy_loop(self.FPS)
        try: 
            game_progress_data = self.game.get_scene_progress_data()
            self.game_view.draw(game_progress_data)
        except:
            scene_init_info_dict = self.game.get_scene_init_data()
            self.game_view = PygameView(scene_init_info_dict)
    def not_done(self)->bool:
        """
        檢查他停了沒
        """
        return self.game.is_running() and (not quit_or_esc())
    
    def reset(self):
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.lives = [0, 3, 3, 3, 3, 3, 3]

        self.game.reset()

        return self.getDataForAllAgent()
    
    def getMapGraph(self, data):
        MapGraph = np.zeros((24, 40))
        for wall in data['walls_info']:
            wallX = int(wall['x'] / 25)
            wallY = int(wall['y'] / 25)
            MapGraph[wallY, wallX] = 1
            
        return MapGraph

    def getDataForAllAgent(self)->dict:
        pass


