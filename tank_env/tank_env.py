import pygame
from mlgame.game.generic import quit_or_esc
from mlgame.view.view import PygameView

import sys
sys.path.append("C:/Users/weiso131/Desktop/gameAI/tank/tank_env")

from src.Game import Game
class tankeEnvBase():
    
    def __init__(self, user_num=6, green_team_num=3, blue_team_num=3, FPS=60, trainMode="normal"):

        # initialize game
        self.frame = 2500
        self.sound = "off"
        self.is_manual = False
        self.FPS = FPS
        self.user_num = user_num
        self.green_team_num = green_team_num
        self.blue_team_num = blue_team_num

        self.game = Game(self.user_num, self.green_team_num, 
                    self.blue_team_num, self.is_manual, self.frame, self.sound, trainMode=trainMode)



            
    
    def update(self, actions:dict):
        self.game.update(actions)

        return self.game.get_data_from_game_to_player()

    def render(self):
        pygame.time.Clock().tick_busy_loop(self.FPS)
        try: 
            game_progress_data = self.game.get_scene_progress_data()
            self.game_view.draw(game_progress_data)
        except:
            scene_init_info_dict = self.game.get_scene_init_data()
            self.game_view = PygameView(scene_init_info_dict)
    def not_done(self):
        return self.game.is_running() and not quit_or_esc()
    
    def reset(self):
        self.game.reset()
        return self.game.get_data_from_game_to_player()

