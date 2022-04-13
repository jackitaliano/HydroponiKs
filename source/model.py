import json
import os
import copy
from pyfirmata import Arduino
from MVCInterfaces import Model

PUMP_PIN = 3
WATER_LEVEL_PIN = 4
COM_PORT = "/dev/cu.usbmodem111301"
class Model(Model):
    plants : dict
    education_modules : dict

    def __init__(self) -> None:
        # self.arduino = MyArduino()
        
        self.load_plant_types()
        self.load_education_modules()

        self.plant_type = ""
        self.water_level = 0
        self.schedule = {}

        self.load_save_state()

    def set_plant_type(self, type):
        self.plant_type = type

    def set_pump_strength(self, strength):
        self.arduino.analog_write(self.arduino.pump_pin, strength)

    def set_schedule(self, schedule):
        self.schedule = schedule

    def get_plant_type(self):
        if not self.plant_type in self.plants: return 'select plant'
        return self.plant_type

    def get_plant_description(self):
        if not self.plant_type in Model.plants: return 'default description'
        return Model.plants[self.plant_type]["description"]

    def get_plant_water(self):
        if not self.plant_type in Model.plants: return 'default water'
        return Model.plants[self.plant_type]["water"]

    def get_plant_nutrients(self):
        if not self.plant_type in Model.plants: return 'default nutrients'
        return Model.plants[self.plant_type]["nutrients"]

    def get_plant_img_file(self):
        if not self.plant_type in Model.plants: return 'default.jpg'
        return Model.plants[self.plant_type]["img_file"]

    def get_plant_schedule(self):
        if not self.plant_type in Model.plants: return {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        return copy.deepcopy(Model.plants[self.plant_type]["schedule"])

    def get_plant_types(self):
        return [key for key in Model.plants]

    def get_schedule(self):
        return copy.deepcopy(self.schedule)

    def get_education_modules(self):
        return copy.deepcopy(Model.education_modules)

    def get_water_level(self):
        return self.arduino.analog_read(self.arduino.water_level_pin)

    def load_plant_types(self):
        with open(os.path.join("data", "plants.json"), 'r') as file:
            Model.plants = json.load(file)

    def load_education_modules(self):
        with open(os.path.join("data", "education.json"), 'r') as file:
            Model.education_modules = json.load(file)

    def load_save_state(self):
        with open(os.path.join("data", "stored_state.json"), 'r') as file:
            state = json.load(file)

            self.plant_type = state["type"]
            self.water_level = state["water_level"]
            self.schedule = state["schedule"]

    def dump_save_state(self):
        state = {
            "type": self.plant_type,
            "water_level": self.water_level,
            "schedule": self.schedule
        }

        with open(os.path.join('data', 'stored_state.json'), 'w') as file:
            json.dump(state, file)

class MyArduino(Arduino):
    def init_serial_monitor(self):
        #try connecting to serial monitor
        try:
            self.board = Arduino(COM_PORT)
            self.pump_pin = self.board.get_pin(f'a:{PUMP_PIN}:o')
            self.water_level_pin = self.board.get_pin(f'a:{WATER_LEVEL_PIN}:o')
            print("Connected successfully!")
        except:
            print('Connection unsuccessful. Quiting...')
            quit()

    def analog_write(pin, val):
        pin.write(val)

    def analog_read(self, pin):
        return pin.read()

