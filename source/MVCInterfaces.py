from abc import ABC, abstractclassmethod
import tkinter as tk
from tkinter import ttk, StringVar

class Model(ABC):
    '''Model for HydroponiKs'''
    @abstractclassmethod
    def set_plant_type(self, type:str) -> None:
        '''Set current plant type selected'''
        pass

    @abstractclassmethod
    def set_schedule(self, schedule: dict) -> None:
        '''Set model schedule to schedule'''
        pass
    
    @abstractclassmethod
    def get_plant_type(self) -> str:
        '''Return current plant type'''
        pass

    @abstractclassmethod
    def get_plant_description(self) -> str:
        '''Return current plant's description'''
        pass

    @abstractclassmethod
    def get_plant_water(self) -> str:
        '''Return current plant's water needs'''
        pass

    @abstractclassmethod
    def get_plant_nutrients(self) -> str:
        '''Return current plant's nutrients needs'''
        pass

    @abstractclassmethod
    def get_plant_img_file(self) -> str:
        '''Return current plant's image file name'''
        pass

    @abstractclassmethod
    def get_plant_schedule(self) -> dict:
        '''Return current plant's default schedule dictionary'''
        pass

    @abstractclassmethod
    def get_plant_types(self) -> list:
        '''Return list of all plant types'''
        pass

    @abstractclassmethod
    def get_schedule(self) -> dict:
        '''Return current schedule dictionary'''
        pass

    @abstractclassmethod
    def get_education_modules(self) -> dict:
        '''Return the dictionary of education modules'''
        pass

    @abstractclassmethod
    def load_plant_types(self) -> None:
        '''Load names of plant types'''
        pass

    @abstractclassmethod
    def load_education_modules(self) -> None:
        '''Load education modules containing text and images'''
        pass

    @abstractclassmethod
    def load_save_state(self) -> None:
        '''Load save state of schedule/plant type from json'''
        pass

    @abstractclassmethod
    def dump_save_state(self) -> None:
        '''Dump save state of schedule/plant type to json'''
        pass

class View(ABC, tk.Frame):
    '''View for HydroponiKs'''
    @abstractclassmethod
    def create_view(self, schedule: dict, current_plant: str, plant_types: list) -> None:
        '''Create new view'''
        pass

    @abstractclassmethod
    def register_observer(self, observer) -> None:
        '''Register observer to view'''
        pass

    @abstractclassmethod
    def set_plant_types(self, types: list) -> None:
        '''Set view plant types (used for menu options)'''
        pass

    @abstractclassmethod
    def update_plant_info(self, type: str, description: str, water: str, nutrients: str, img_file: str) -> None:
        '''Update plant information tab'''
        pass

    @abstractclassmethod
    def update_schedule(self, schedule: dict) -> None:
        '''Update schedule tab'''
        pass

class Controller(ABC):
    '''Controller for HydroponiKs'''
    @abstractclassmethod
    def update_view_to_match_model(self) -> None:
        '''Update all view components to match model data'''
        pass

    @abstractclassmethod
    def update_plant_type(self, type: str) -> None:
        '''Update model's plant type'''
        pass

    @abstractclassmethod
    def process_water_event(self) -> None:
        '''Turn on water now'''
        pass

    @abstractclassmethod
    def process_menu_change_event(self, type) -> None:
        '''Change plant type and update view'''
        pass

    @abstractclassmethod
    def process_load_plant_schedule_event(self) -> None:
        '''Load plant default schedule and update view'''
        pass

    @abstractclassmethod
    def process_clear_schedule_event(self) -> None:
        '''Clear schedule and update view'''
        pass

    @abstractclassmethod
    def process_schedule_change_event(self) -> None:
        '''Add new time to schedule or remove from schedule if already there'''
        pass

class Event(ABC):
    '''Simple event object with source and event'''
    @abstractclassmethod
    def source(self) -> str:
        '''Get source of event'''
        pass

    @abstractclassmethod
    def __repr__(self) -> str:
        '''Default representation as string of event'''
        pass

class Frame(ABC, tk.Frame):
    '''Generic Frame with methods to create tk objects and default action performed'''
    @abstractclassmethod
    def create_button(self, text: str, row: int, col: int, event: Event, border: bool, color: str, font_size: int, fill: bool) -> tk.Label:
        '''Create and return new tk button'''
        pass

    @abstractclassmethod
    def create_label(self, text: str, row: int, col: int) -> ttk.Label:
        '''Create and return new ttk label'''
        pass

    @abstractclassmethod
    def create_menu(self, row: int, col: int, default: StringVar, options: list, event: Event) -> ttk.OptionMenu:
        '''Create and return new ttk option menu with plant types set as options'''
        pass

    @abstractclassmethod
    def create_img(self, row: int, col: int, width: int, height: int, img_file: str) -> ttk.Label:
        '''Create and return new ttk label containing an image'''
        pass

    @abstractclassmethod
    def create_button_table(self, row: int, col: int, table: list) -> tk.Frame:
        '''Create and return a table of buttons with x/y axises'''
        pass

    @abstractclassmethod
    def action_performed() -> None:
        '''Default action to call master action performed'''
        pass