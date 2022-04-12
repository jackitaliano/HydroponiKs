from abc import ABC, abstractclassmethod

class Controller(ABC):
    @abstractclassmethod
    def update_view_to_match_model(self):
        pass

class Controller1(Controller):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

        self.update_view_to_match_model()

    def update_view_to_match_model(self):
        type = self.model.get_plant_type()
        description = self.model.get_plant_description()
        water = self.model.get_plant_water()
        nutrients = self.model.get_plant_nutrients()
        img_file = self.model.get_plant_img_file()

        # self.view.set_plant_info(type, description, water, nutrients, img_file)

        

    def update_plant_type(self, type):
        self.model.set_plant_type(type)
