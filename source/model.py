import json
import os
import copy
from pyfirmata import Arduino, util
from MVCInterfaces import Model

class Model(Model):
    plants : dict
    education_modules : dict

    def __init__(self) -> None:
        self.arduino = MyArduino()

        self.arduino_active = self.arduino.active
        
        # Load plant types and education modules (remain static)
        self.load_plants()
        self.load_education_modules()

        # Declare plant type, water level, and schedule
        self.plant_type : str
        self.water_level : int
        self.schedule : dict
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
        self.plants[self.plant_type]['custom_schedule'] = copy.deepcopy(self.schedule)

    def set_time(self, time):
        self.time = time

    def set_pump_active_status(self, status):
        self.pump_active_status = status

    def set_manual_override_status(self, status):
        self.manual_overridden_status = status

    def set_pump_status(self, status):
        if not self.arduino_active: return

        self.arduino.digital_write(self.arduino.pump_pin, status)

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
        if not self.plant_type in Model.plants: return {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        return Model.plants[self.plant_type]["custom_schedule"]

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

        level = self.arduino.analog_read(self.arduino.water_level_pin)

        if level == None or level < 0.1: self.water_level = "Low"
        if level >= 0.1 and level < .23: self.water_level = "Medium"
        if level >= .22: self.water_level = "High"

    def load_plants(self):
        # Load plants from json to plant dict
        with open(os.path.join("data", "plants.json"), 'r') as file:
            Model.plants = json.load(file)

    def load_education_modules(self):
        # Load education modules from json to education modules dict
        with open(os.path.join("data", "education.json"), 'r') as file:
            Model.education_modules = json.load(file)

    def load_save_state(self):
        # Load save state (plant type, water level, schedule)
        with open(os.path.join("data", "stored_state.json"), 'r') as file:
            state = json.load(file)

            self.plant_type = state["type"]
            self.water_level = state["water_level"]
            self.schedule = state["schedule"]

    def dump_save_state(self):
        # Dump save state (plant type, water level, schedule)
        state = {
            "type": self.plant_type,
            "water_level": self.water_level,
            "schedule": self.schedule
        }
        
        with open(os.path.join('data', 'stored_state.json'), 'w') as file:
            json.dump(state, file, indent=4)

        # Dump plants state (for custom schedules)
        with open(os.path.join('data', 'plants.json'), 'w') as file:
            json.dump(Model.plants, file, indent=4)

class MyArduino(Arduino):
    def __init__(self):
        #try connecting to serial monitor
        try:
            self.config()

            if not self.active:
                raise self.ArduinoException("Arduino Inactive")

            self.board = Arduino(self.com_port)

            it = util.Iterator(self.board)
            it.start()

            self.water_level_pin = self.board.get_pin(self.water_level_pin_config)
            self.pump_pin= self.board.get_pin(self.pump_pin_config)

            self.active = True
            print("Connected successfully!")

        except self.ArduinoException as error:
            print(f"Connecting unsuccesful: {error}")
            print("Proceeding without connection...")
            self.active = False

        except:
            print('Connection unsuccessful. Quitting...')
            quit()

    def config(self):
        with open(os.path.join('data', 'arduino_config.json'), 'r') as file:
            config = json.load(file)

            active = config['active']
            if active == "FALSE":
                self.active = False
            elif active == "TRUE":
                self.active = True
            else:
                raise self.ArduinoException("Invalid Arduino Active Status")

            self.com_port = config['com_port']
            self.pump_strength = config['pump_strength']

            self.pump_pin_config = config['pump_pin']
            self.water_level_pin_config = config['water_level_pin']
            

    def analog_write(pin, val):
        pin.write(val)

    def analog_read(self, pin):
        return pin.read()

    def digital_write(self, pin, val):
        pin.write(val)

    class ArduinoException(Exception):
        pass
