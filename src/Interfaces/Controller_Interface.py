from abc import ABC, abstractclassmethod

class Controller(ABC):
    '''Controller for HydroponiKs'''
    @abstractclassmethod
    def update_view_to_match_model(self) -> None:
        '''Update all view components to match model data'''
        
    @abstractclassmethod
    def update_plant_type(self, type: str) -> None:
        '''Update model's plant type'''
        
    @abstractclassmethod
    def update_time(self) -> None:
        '''Update time of model (day,time)'''

    @abstractclassmethod
    def handle_time(self) -> None:
        '''Handle times for turning on/off pump in event of schedule'''

    @abstractclassmethod
    def process_menu_change_event(self, type) -> None:
        '''Change plant type and update view'''
        
    @abstractclassmethod
    def process_load_plant_default_schedule_event(self) -> None:
        '''Load plant default schedule and update view'''
        
    @abstractclassmethod
    def process_load_plant_custom_schedule_event(self) -> None:
        '''Load plant custom schedule and update view'''
        
    @abstractclassmethod
    def process_save_plant_custom_schedule_event(self) -> None:
        '''Save plant custom schedule and update view'''

    @abstractclassmethod
    def process_clear_schedule_event(self) -> None:
        '''Clear schedule and update view'''
        
    @abstractclassmethod
    def process_schedule_change_event(self) -> None:
        '''Add new time to schedule or remove from schedule if already there'''

    @abstractclassmethod
    def process_turn_on_pump_event(self, manual: bool) -> None:
        '''Turn on pump and update manual override if manual'''

    @abstractclassmethod
    def process_turn_off_pump_event(self, manual: bool) -> None:
        '''Turn off pump and update manual override if manual'''     