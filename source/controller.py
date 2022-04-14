from MVCInterfaces import Controller
from datetime import datetime

PUMP_STRENGTH = 100
TIME_OFFSET_FOR_TESTING = 30
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
        current_time = self.model.get_time()
        water_level = self.model.get_water_level()

        #get education modules
        education = self.model.get_education_modules()

        #send updates
        self.view.update_plant_info(type, description, water, nutrients, img_file)
        self.view.update_controls(schedule, current_time, water_level)
        self.view.update_education_modules(education)

    def update_plant_type(self, type):
        self.model.set_plant_type(type)

    def update_time(self):
        weekday = datetime.today().strftime('%A')[0:3]
        # time = datetime.now().hour
        time = datetime.now().minute
        self.model.set_time((weekday, time - TIME_OFFSET_FOR_TESTING))

    def update_water_level(self):
        water_level = self.model.get_water_level()
        #TODO update water level in view

    def handle_time(self):
        self.update_time()

        weekday, time = self.model.get_time()
        schedule = self.model.get_schedule()

        if time in schedule[weekday]:
            self.process_turn_on_pump_event()
        elif time not in schedule[weekday]:
            self.process_turn_off_pump_event()

        self.model.update_water_level()

        self.update_view_to_match_model()

    def process_menu_change_event(self, type):
        # Update plant type
        self.update_plant_type(type)

        # Update view
        self.update_view_to_match_model()

    def process_load_plant_default_schedule_event(self):
        # Set new schedule
        self.model.set_schedule(self.model.get_plant_default_schedule())
        self.model.set_manual_override_status(False)

        # Update view
        self.update_view_to_match_model()

    def process_load_plant_custom_schedule_event(self):
        # Set new schedule
        self.model.set_schedule(self.model.get_plant_custom_schedule())
        self.model.set_manual_override_status(False)

        # Update view
        self.update_view_to_match_model()

    def process_save_plant_custom_schedule_event(self):
        # Set new schedule
        self.model.set_plant_custom_schedule()

        # Update view
        self.update_view_to_match_model()

    def process_clear_schedule_event(self):
        # Create empty schedule
        empty_schedule = {"Sun":[],"Mon":[],"Tue":[],"Wed":[],"Thu":[],"Fri":[],"Sat":[]}
        # Set new schedule
        self.model.set_schedule(empty_schedule)
        self.model.set_manual_override_status(False)

        # Update view
        self.update_view_to_match_model()

    def process_schedule_change_event(self, new_time):
        # Split event ("day,time") to day, time
        day, time = new_time.split(",")
        time = int(time)
        # Get day schedule
        schedule = self.model.get_schedule()
        day_schedule = schedule[day]

        # Add to schedule if not there, remove from schedule if there (toggle)
        if time not in day_schedule:
            day_schedule.append(time)
        else:
            day_schedule = [x for x in day_schedule if x != time]
        
        # Update day schedule in schedule
        schedule[day] = day_schedule

        # Set new schedule
        self.model.set_schedule(schedule)

        self.model.set_manual_override_status(False)

        # Update view
        self.update_view_to_match_model()

    def process_turn_on_pump_event(self, manual=False):
        # Set pump strength to PUMP_STRENGTH
        # self.model.set_pump_strength(PUMP_STRENGTH)

        pump_active = self.model.get_pump_active_status()
        manual_override = self.model.get_manual_override_status()

        if pump_active: return
        if manual_override and not manual: return

        if manual:
            self.model.set_manual_override_status(True)

        self.model.set_pump_active_status(True)
        self.model.turn_on_led()
        print("Turning on pump...")
    
    def process_turn_off_pump_event(self, manual=False):
        # Set pump strength to 0
        # self.model.set_pump_strength(0)

        pump_active = self.model.get_pump_active_status()
        manual_override = self.model.get_manual_override_status()

        if not pump_active: return
        if manual_override and not manual: return

        if manual:
            self.model.set_manual_override_status(True)

        self.model.set_pump_active_status(False)
        self.model.turn_off_led()
        print("Turning off pump...")

    def exit(self):
        self.model.dump_save_state()
        self.model.turn_off_led()
        self.process_turn_off_pump_event()
