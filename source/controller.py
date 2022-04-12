from abc import ABC, abstractclassmethod
from pyfirmata import Arduino

PUMP_STRENGTH = 100

class Controller(ABC):
    @abstractclassmethod
    def update_view_to_match_model(self):
        pass
class Controller(Controller):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

        #self.update_view_to_match_model()

    def update_view_to_match_model(self):
        #get plant info
        type = self.model.get_plant_type()
        description = self.model.get_plant_description()
        water = self.model.get_plant_water()
        nutrients = self.model.get_plant_nutrients()
        img_file = self.model.get_plant_img_file()

        #get schedule
        schedule = self.model.get_schedule()

        #send updates
        # self.view.update_plant_info(type, description, water, nutrients, img_file)
        self.view.update_schedule(schedule)

    def turn_on_pump(self):
        self.model.set_pump_strength(PUMP_STRENGTH)

    def turn_off_pump(self):
        self.model.set_pump_strength(0)

    def process_water_event(self):
        print('water')

    def update_water_level(self):
        water_level = self.model.get_water_level()
        #TODO update water level in view

    def update_plant_type(self, type):
        self.model.set_plant_type(type)


