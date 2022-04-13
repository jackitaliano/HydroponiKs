from pyfirmata import Arduino
from MVCInterfaces import Controller

PUMP_STRENGTH = 100
class Controller(Controller):
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def update_view_to_match_model(self):
        #get plant info
        type = self.model.get_plant_type()
        description = self.model.get_plant_description()
        water = self.model.get_plant_water()
        nutrients = self.model.get_plant_nutrients()
        img_file = self.model.get_plant_img_file()

        #get schedule
        schedule = self.model.get_schedule()

        #get education modules
        education = self.model.get_education_modules()

        #send updates
        self.view.update_plant_info(type, description, water, nutrients, img_file)
        self.view.update_schedule(schedule)
        self.view.update_education_modules(education)

    def update_water_level(self):
        water_level = self.model.get_water_level()
        #TODO update water level in view

    def update_plant_type(self, type):
        self.model.set_plant_type(type)

    def process_turn_on_pump(self):
        self.model.set_pump_strength(PUMP_STRENGTH)

    def process_turn_off_pump(self):
        self.model.set_pump_strength(0)

    def process_water_event(self):
        print('water')

        self.update_view_to_match_model()

    def process_menu_change_event(self, type):
        self.update_plant_type(type)

        self.update_view_to_match_model()

    def process_load_plant_schedule_event(self):
        self.model.set_schedule(self.model.get_plant_schedule())

        self.update_view_to_match_model()

    def process_clear_schedule_event(self):
        empty_schedule = {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        self.model.set_schedule(empty_schedule)

        self.update_view_to_match_model()

    def process_schedule_change_event(self, new_time):
        day, time = new_time.split(",")
        time = int(time)
        schedule = self.model.get_schedule()
        day_schedule = schedule[day]

        if time not in day_schedule:
            day_schedule.append(time)
        else:
            day_schedule = [x for x in day_schedule if x != time]
            
        schedule[day] = day_schedule

        self.model.set_schedule(schedule)

        self.update_view_to_match_model()


