import math
from collections import OrderedDict

class Environment():
    def __init__(self) -> None:                                                                        
        self.action_mapping = [["NONE"], ["TURN_RIGHT"], ["FORWARD"], ["BACKWARD"]]
        self.n_actions = len(self.action_mapping)
        
        self.action = 0 
        self.observation = 0
        self.pre_reward = 0
    
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
        
        reward = self.__get_reward(action, observation)
                
        done = self.scene_info["status"] != "GAME_ALIVE"            

        info = {}

        return observation, reward, done, info
    
    def __get_obs(self, scene_info):      

        FaceMap = { 0: "LEFT" ,45: "DOWNLEFT" ,90: "DOWN" ,135:"DOWNRIGHT"
                   ,180:"RIGHT" ,225:"UPRIGHT" ,270:"UP" ,315:"UPLEFT"}

        if abs(scene_info["competitor_info"][0]["x"] - scene_info["x"]) < 8:
            Target_x = "CORRECT"
        elif scene_info["competitor_info"][0]["x"] - scene_info["x"] > 0:
            Target_x = "LEFT"
        else:
            Target_x = "UP"
        
        if abs(scene_info["competitor_info"][0]["y"] - scene_info["y"]) < 8:
            Target_y = "CORRECT"
        elif scene_info["competitor_info"][0]["y"] - scene_info["y"] > 0:
            Target_y = "UP"
        else:
            Target_y = "DOWN"
        
        observation = {"Face": FaceMap[abs(scene_info["angle"])], "Target_x": Target_x, "Target_y": Target_y}
            
        return observation
        
        
    
    def __get_reward(self, action: int , observation: int):        
        reward = 0
        if observation["Target_y"] != "CORRECT":
            if observation["Face"] != "UP":
                if self.action_mapping[action] != ["TURN_RIGHT"]:
                    reward -= 100                                  
                else:
                    reward += 10                    
            elif observation["Target_y"] ==  "DOWN":
                if self.action_mapping[action] != ["FORWARD"]:
                    reward -= 10
                else:
                    reward += 10
            else:
                if self.action_mapping[action] != ["BACKWARD"]:
                    reward -= 10
                else:
                    reward += 10
        
        elif observation["Target_x"] != "CORRECT":
            if observation["Face"] != "LEFT":
                if self.action_mapping[action] != ["TURN_RIGHT"]:
                    reward -= 100
                else:
                    reward += 10
            elif observation["Target_x"] ==  "RIGHT":                
                if self.action_mapping[action] != ["FORWARD"]:
                    reward -= 10
                else:
                    reward += 100
            else:
                if self.action_mapping[action] != ["BACKWARD"]:
                    reward -= 10
                else:
                    reward += 100
        
            

        # print(f"reward: {reward:5d} obs: {observation} action: {self.action_mapping[action]}")

        return reward

    def __find_closest_wall(self, user_pos, walls):
        min_distance = float('inf')
        closest_wall = None

        for wall in walls:
            distance = self.__calculate_distance(user_pos, wall)
            if distance < min_distance:
                min_distance = distance
                closest_wall = wall

        return closest_wall
    
    def __calculate_distance(self, point1: list, point2: list)->float:        
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    