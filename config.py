import json


# Load Config Settings
with open("config.json") as json_file:
    config_data = json.load(json_file)


# Constants
WIDTH = config_data["WIDTH"]
HEIGHT = config_data["HEIGHT"]
FPS = config_data["FPS"]
ENEMY_TIMER = config_data["ENEMY_TIMER"]
SHOOTING_TIMER = config_data["SHOOTING_TIMER"]
RUN = False



    


     
