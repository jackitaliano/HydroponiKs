from abc import ABC, abstractclassmethod
import tkinter as tk
from tkinter import ttk, StringVar

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
        