from abc import ABC, abstractclassmethod
import tkinter as tk

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