from abc import ABC, abstractclassmethod
import json
import os

class Model(ABC):
    @abstractclassmethod
    def load_plant_types(self):
        pass

    @abstractclassmethod
    def load_save_state(self):
        pass

    @abstractclassmethod
    def save_state(self):
        pass


class Model1(Model):
    plants : dict

    def __init__(self) -> None:
        
        self.load_plant_types()

        self.plant_type = ""
        self.water_level = 0
        self.schedule = []

        self.load_save_state()

    def set_plant_type(self, type):
        self.plant_type = type

    def get_plant_type(self):
        if not self.plant_type in self.plants: return 'select plant'
        return self.plant_type

    def get_plant_description(self):
        if not self.plant_type in self.plants: return 'default description'
        return self.plants[self.plant_type]["description"]

    def get_plant_water(self):
        if not self.plant_type in self.plants: return 'default water'
        return self.plants[self.plant_type]["water"]

    def get_plant_nutrients(self):
        if not self.plant_type in self.plants: return 'default nutrients'
        return self.plants[self.plant_type]["nutrients"]

    def get_plant_img_file(self):
        if not self.plant_type in self.plants: return 'default.jpg'
        return self.plants[self.plant_type]["img_file"]

    def get_plant_types(self):
        return [key for key in self.plants]

    def get_schedule(self):
        return self.schedule

    def load_plant_types(self):
        with open(os.path.join("plants", "plants.json"), 'r') as file:
            Model1.plants = json.load(file)

    def load_save_state(self):
        with open(os.path.join("plants", "stored_state.json"), 'r') as file:
            state = json.load(file)

            self.plant_type = state["type"]
            self.water_level = state["water_level"]
            self.schedule = state["schedule"]

    def save_state(self):
        state = {
            "type": self.plant_type,
            "water_level": self.water_level,
            "schedule": self.schedule
        }

        with open(os.path.join('plants', 'stored_state.json'), 'w') as file:
            json.dump(state, file)

