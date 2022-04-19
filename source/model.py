import os
import copy
from Interfaces.Model_Interface import Model
from arduino import CustomArduino as Arduino
from config import DEV_CONFIG
import json_methods

EDUCATION_FILE_PATH = os.path.join(DEV_CONFIG['data_folder'], DEV_CONFIG['education_file'])
PLANTS_FILE_PATH = os.path.join(DEV_CONFIG['data_folder'], DEV_CONFIG['plants_file'])
SAVE_FILE_PATH = os.path.join(DEV_CONFIG['data_folder'], DEV_CONFIG['save_file'])

class Model(Model):
    plants : dict
    education_modules : dict

    def __init__(self) -> None:
        self.arduino = Arduino()

        self.arduino_active = self.arduino.active
        
        # Load plant types and education modules (remain static)
        self.load_plants()
        self.load_education_modules()

        # Declare plant type, water level, and schedule
        self.plant_type : str
        self.water_level : int
        self.schedule : dict
        self.custom_schedules: dict
        self.time = (0,0)
        self.pump_active_status = False
        self.manual_overridden_status = False

        # Load previous save state
        self.load_save_state()

    def set_plant_type(self, type):
        self.plant_type = type

    def set_schedule(self, schedule):
        self.schedule = schedule

    def set_plant_custom_schedule(self):
        # Set current plant custom schedule to a deepcopy of schedule (avoids aliasing)
        self.custom_schedules[self.plant_type] = copy.deepcopy(self.schedule)

    def set_time(self, time):
        self.time = time

    def set_pump_active_status(self, status):
        self.pump_active_status = status

    def set_manual_override_status(self, status):
        self.manual_overridden_status = status

    def set_pump_status(self, status):
        if not self.arduino_active: return

        self.arduino.write_to_pin(self.arduino.pump_pin, status)

    def get_time(self):
        return self.time

    def get_pump_active_status(self):
        return self.pump_active_status
    
    def get_manual_override_status(self):
        return self.manual_overridden_status

    def get_plant_type(self):
        # Return plant type or default
        if not self.plant_type in self.plants: return 'select plant'
        return self.plant_type

    def get_plant_description(self):
        # Return plant description or default
        if not self.plant_type in Model.plants: return 'default description'
        return Model.plants[self.plant_type]["description"]

    def get_plant_water(self):
        # Return plant water or default
        if not self.plant_type in Model.plants: return 'default water'
        return Model.plants[self.plant_type]["water"]

    def get_plant_nutrients(self):
        # Return plant nutrients or default
        if not self.plant_type in Model.plants: return 'default nutrients'
        return Model.plants[self.plant_type]["nutrients"]

    def get_plant_img_file(self):
        # Return plant image file or default
        if not self.plant_type in Model.plants: return 'default.jpg'
        return Model.plants[self.plant_type]["img_file"]

    def get_plant_default_schedule(self):
        # Return plant schedule or default
        if not self.plant_type in Model.plants: return {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        return copy.deepcopy(Model.plants[self.plant_type]["default_schedule"])

    def get_plant_custom_schedule(self):
        # Return plant schedule or default
        if not self.plant_type in self.custom_schedules: return {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        return self.custom_schedules[self.plant_type]

    def get_plant_types(self):
        # Return list of each plant type
        return [key for key in Model.plants]

    def get_schedule(self):
        # Return deepcopy of schedule (avoid aliasing)
        return copy.deepcopy(self.schedule)

    def get_education_modules(self):
        # Return deepcopy of modules (avoid aliasing)
        return copy.deepcopy(Model.education_modules)

    def get_water_level(self):
        return self.water_level

    def update_water_level(self):
        # Return water level read from arduino
        if not self.arduino_active: 
            self.water_level = "NOT CONNECTED"
            return

        level = self.arduino.read_from_pin(self.arduino.water_level_pin)

        if level == None or level < 0.1: self.water_level = "Low"
        if level >= 0.1 and level < .23: self.water_level = "Medium"
        if level >= .22: self.water_level = "High"

    def load_plants(self):
        # Load plants from json to plant dict
        Model.plants = json_methods.load_json(PLANTS_FILE_PATH)

    def load_education_modules(self):
        # Load education modules from json to education modules dict
        Model.education_modules = json_methods.load_json(EDUCATION_FILE_PATH)

    def load_save_state(self):
        # Load save state (plant type, water level, schedule)
        state = json_methods.load_json(SAVE_FILE_PATH)

        self.plant_type = state["type"]
        self.water_level = state["water_level"]
        self.schedule = state["schedule"]
        self.custom_schedules = state["custom_schedules"]

    def dump_save_state(self):
        # Dump save state (plant type, water level, schedule)

        state = {
            "type": self.plant_type,
            "water_level": self.water_level,
            "schedule": self.schedule,
            "custom_schedules": self.custom_schedules
        }
        
        json_methods.dump_json(state, SAVE_FILE_PATH, pretty=True)
