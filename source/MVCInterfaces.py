from abc import ABC, abstractclassmethod
import tkinter as tk
from tkinter import ttk, StringVar

class Model(ABC):
    '''Model for HydroponiKs'''
    @abstractclassmethod
    def set_plant_type(self, type:str) -> None:
        '''Set current plant type selected'''

    @abstractclassmethod
    def set_schedule(self, schedule: dict) -> None:
        '''Set model schedule to schedule'''

    @abstractclassmethod
    def set_plant_custom_schedule(self) -> None:
        '''Set current plant custom schedule to current schedule'''
        
    @abstractclassmethod
    def set_pump_active_status(self, status: bool) -> None:
        '''Set active status of pump (True/False == On/Off)'''

    @abstractclassmethod
    def set_manual_override_status(self, status: bool) -> None:
        '''Set status of manual override'''

    @abstractclassmethod
    def set_pump_status(self, status: int) -> None:
        '''Set strength of pump on arduino'''

    @abstractclassmethod
    def get_time(self) -> tuple:
        '''Return current (day,time)'''

    @abstractclassmethod
    def get_pump_active_status(self) -> bool:
        '''Retrun current active status of pump (True/False == On/Off)''' 

    @abstractclassmethod
    def get_manual_override_status(self) -> bool:
        '''Return status of manual override'''  

    @abstractclassmethod
    def get_plant_description(self) -> str:
        '''Return current plant's description'''
    
    @abstractclassmethod
    def get_plant_type(self) -> str:
        '''Return current plant type'''

    @abstractclassmethod
    def get_plant_water(self) -> str:
        '''Return current plant's water needs'''
        
    @abstractclassmethod
    def get_plant_nutrients(self) -> str:
        '''Return current plant's nutrients needs'''
        
    @abstractclassmethod
    def get_plant_img_file(self) -> str:
        '''Return current plant's image file name'''
        
    @abstractclassmethod
    def get_plant_default_schedule(self) -> dict:
        '''Return current plant's default schedule dictionary'''
        
    @abstractclassmethod
    def get_plant_custom_schedule(self) -> dict:
        '''Return current plant's custom schedule dictionary'''
        
    @abstractclassmethod
    def get_plant_types(self) -> list:
        '''Return list of all plant types'''
        
    @abstractclassmethod
    def get_schedule(self) -> dict:
        '''Return current schedule dictionary'''
        
    @abstractclassmethod
    def get_education_modules(self) -> dict:
        '''Return the dictionary of education modules'''

    @abstractclassmethod
    def get_water_level(self) -> str:
        '''Return water level from arduino'''

    @abstractclassmethod
    def update_water_level(self) -> None:
        '''Update water level from arduino'''
        
    @abstractclassmethod
    def load_plants(self) -> None:
        '''Load names of plant types'''
        
    @abstractclassmethod
    def load_education_modules(self) -> None:
        '''Load education modules containing text and images'''
     
    @abstractclassmethod
    def load_save_state(self) -> None:
        '''Load save state of schedule/plant type from json'''
        
    @abstractclassmethod
    def dump_save_state(self) -> None:
        '''Dump save state of schedule/plant type to json''' 

class View(ABC, tk.Frame):
    '''View for HydroponiKs'''
    @abstractclassmethod
    def create_view(self, schedule: dict, current_plant: str, plant_types: list) -> None:
        '''Create new view'''
        
    @abstractclassmethod
    def register_observer(self, observer) -> None:
        '''Register observer to view'''
        
    @abstractclassmethod
    def set_plant_types(self, types: list) -> None:
        '''Set view plant types (used for menu options)'''
        
    @abstractclassmethod
    def update_plant_info(self, type: str, description: str, water: str, nutrients: str, img_file: str) -> None:
        '''Update plant information tab'''
        
    @abstractclassmethod
    def update_controls(self, schedule: dict, current_time: tuple, water_level: int) -> None:
        '''Update schedule tab'''
        
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

class Event(ABC):
    '''Simple event object with source and event'''
    @abstractclassmethod
    def source(self) -> str:
        '''Get source of event'''
        

    @abstractclassmethod
    def __repr__(self) -> str:
        '''Default representation as string of event'''
        

class Frame(ABC, tk.Frame):
    '''Generic Frame with methods to create tk objects and default action performed'''
    @abstractclassmethod
    def create_button(self, text: str, row: int, col: int, event: Event, border: bool, color: str, font_size: int, fill: bool) -> tk.Label:
        '''Create and return new tk button'''
        

    @abstractclassmethod
    def create_label(self, text: str, row: int, col: int) -> ttk.Label:
        '''Create and return new ttk label'''
        

    @abstractclassmethod
    def create_menu(self, row: int, col: int, default: StringVar, options: list, event: Event) -> ttk.OptionMenu:
        '''Create and return new ttk option menu with plant types set as options'''
        

    @abstractclassmethod
    def create_img(self, row: int, col: int, width: int, height: int, img_file: str) -> ttk.Label:
        '''Create and return new ttk label containing an image'''
        

    @abstractclassmethod
    def create_button_table(self, row: int, col: int, table: list) -> tk.Frame:
        '''Create and return a table of buttons with x/y axises'''
        

    @abstractclassmethod
    def action_performed() -> None:
        '''Default action to call master action performed'''
        