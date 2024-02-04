import math
from collections import OrderedDict

class Environment():
    def __init__(self) -> None:                                                                        
        self.action_mapping = [["NONE"], ["TURN_LEFT"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"]]
        self.n_actions = len(self.action_mapping)
        
        self.action = 0 
        self.observation = 0
        self.pre_reward = 0
        self.pre_scene_info = {"x":0, "y":0}
        
    def set_scene_info(self, Scene_info: dict):
        """
        Stores the given scene information into the environment.

        Parameters:
        scene_info (dict): A dictionary containing environment information.
        """
        self.scene_info = Scene_info        
    
    def reset(self):
        """
        Resets the environment and returns the initial observation.

        Returns:
        observation: The initial state of the environment after reset.
        """
        observation = self.__get_obs(self.scene_info)

        return observation
    
    def step(self, action: int):   
        """
        Executes a given action in the environment and returns the resulting state.

        Parameters:
        action (int): The action to be performed, representing the squid's movement.

        Returns:
        observation: The current state of the environment after the action.
        reward (int): The reward obtained as a result of performing the action.
        done (bool): Indicates whether the game has ended (True if ended, False otherwise).
        info (dict): Additional information about the current state.
        """
        reward = 0
        observation = self.__get_obs(self.scene_info)                  
        
        reward = self.__get_reward(observation)
                
        done = self.scene_info["status"] != "GAME_ALIVE"            

        info = {}

        return observation, reward, done, info
    
    ##########  to do  ##########
    def __get_obs(self, scene_info):      

        FaceMap = { 0: "LEFT" ,45: "DOWNLEFT" ,90: "DOWN" ,135:"DOWNRIGHT"
                   ,180:"RIGHT" ,225:"UPRIGHT" ,270:"UP" ,315:"UPLEFT", 360: "LEFT"}

    
        observation = {"Face": FaceMap[abs(scene_info["angle"])]}
        
        
        return observation
        
        
    ##########  to do  ##########
    def __get_reward(self):        
        reward = 0        
        

        return reward
    