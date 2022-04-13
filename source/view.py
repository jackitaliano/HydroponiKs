from abc import ABC, abstractclassmethod
from doctest import master
import os
import tkinter as tk
from tkinter import StringVar, ttk
import tkmacosx as tkm
from Frames import Frame, Event

class View(ABC, tk.Frame):
    @abstractclassmethod
    def create_view():
        pass

    @abstractclassmethod
    def register_observer():
        pass

    @abstractclassmethod
    def set_plant_types():
        pass

    @abstractclassmethod
    def update_plant_info():
        pass

    @abstractclassmethod
    def update_schedule():
        pass

class View(View):
    def __init__(self, master):
        super().__init__(master)
        
        self.controller : object
        self.grid(sticky="nsew",row=0, column=0)

    def create_view(self, schedule, current_plant, plant_types):

        tabControl = ttk.Notebook(self)

        self.control_tab = ControlFrame(self, tabControl, schedule, row=0, col=0)
        # self.plant_info_tab = ttk.Frame(tabControl)
        self.plant_info_tab = PlantInfoFrame(self, tabControl, current_plant, plant_types, row=0, col=0)
        self.education_tab = ttk.Frame(tabControl)

        tabControl.add(self.control_tab, text ='Controls')
        tabControl.add(self.plant_info_tab, text ='Plant Info')
        tabControl.add(self.education_tab, text ='Education')
        tabControl.pack(expand = 1, fill='both')

    def register_observer(self, observer):
        self.controller = observer

    def set_plant_types(self, types):
        self.plant_types = types
        
    def update_schedule(self, schedule):
        self.control_tab.schedule = schedule

        self.control_tab.schedule_frame = self.control_tab.ScheduleFrame(master=self.control_tab, row=1, col=0)

    def update_plant_info(self, type, description, water, nutrients, img_file):
        self.plant_info_tab.plant_menu_var.set(type)
        self.plant_info_tab.information_frame.plant_description.config(text=description)
        self.plant_info_tab.information_frame.plant_water.config(text=water)
        self.plant_info_tab.information_frame.plant_nutrients.config(text=nutrients)
        self.plant_info_tab.selection_frame.create_img(row=1, col=0, width=250, height=250, img_file=img_file)
class ControlFrame(Frame):
    def __init__(self, root, master, schedule, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
        self.schedule = schedule
        self.root = root

        #water level label
        self.water_label = self.create_label(text="Water level: 100", row=0, col=0)

        #schedule 
        self.schedule_frame = self.ScheduleFrame(master=self, row=1, col=0)

        #frame containing water now button
        self.water_now_frame = Frame(self, 2, 0)
        self.water_now_frame.grid_columnconfigure(0, weight='1')

        #water button
        self.water_button = self.water_now_frame.create_button(text="Water Now", row=0, col=0, event=Event("Control", "water_now"))
        self.water_button.config(width='20')
        self.water_button.grid_rowconfigure(0, weight='1')

        self.water_button = self.water_now_frame.create_button(text="Load Plant Schedule", row=0, col=1, event=Event("Control", "load_schedule"))
        self.water_button.config(width='20')
        self.water_button.grid_rowconfigure(0, weight='1')

        self.grid_rowconfigure(0, weight=1) #water level
        self.grid_rowconfigure(1, weight=3) #schedule
        self.grid_rowconfigure(2, weight=1) #water now button
        self.grid_columnconfigure(0, weight=1)
        self.grid(row= 0, column =0, sticky="nsew")

    def action_performed(self, e):
        if e.source() == 'Control':
            if str(e) == 'water_now':
                self.root.controller.process_water_event()
            if str(e) == 'load_schedule':
                self.root.controller.process_load_plant_schedule_event()

        elif e.source() == 'Schedule':
            self.root.controller.process_schedule_change_event(str(e))

    class ScheduleFrame(Frame): 
        def __init__(self, master, row=0, col=0, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            #events

            #title
            self.title = ttk.Label(self, text="Schedule")
            self.title.grid(row=0)

            #table of schedule
            self.table = self.update_table_from_schedule(master.schedule)
            self.schedule_frame = self.create_button_table(1, 0, self.table)

            self.grid_rowconfigure(0, weight=1) #title
            self.grid_rowconfigure(1, weight=12) #table
            self.grid_columnconfigure(0, weight=1)

        def update_table_from_schedule(self, schedule):
            table = [[0] * 25 for _ in range(7)]
            table.insert(0, [x - 1 for x in range (25)])

            for i, key in enumerate(schedule):
                table[i+1][0] = key
                for x in schedule[key]: table[i+1][x + 1] = 1

            return table
class PlantInfoFrame(Frame):
    def __init__(self, root, master, plant_menu_var, plant_types, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
        self.root = root

        self.plant_menu_var = StringVar(self)
        self.plant_menu_var.set(plant_menu_var)
        self.plant_types = plant_types

        self.selection_frame = self.SelectionFrame(self, row=0, col=0)
        self.information_frame = self.InformationFrame(self, row=0, col=1)

        self.grid_columnconfigure(0, weight='1') #selection
        self.grid_columnconfigure(1, weight='1') #information
        self.grid_rowconfigure(0, weight='1')

    def action_performed(self, e):
        if e.source() == 'Selection':
            if str(e) == 'menu_change':
                self.root.controller.process_menu_change_event(self.plant_menu_var.get())

    class SelectionFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            self.plant_img = self.create_img(row=1, col=0, width=250, height=250, img_file="default.jpg")
            self.master.plant_dropdown = self.create_menu(row=2, col=0, default=master.plant_menu_var, options=master.plant_types, event=Event("Selection", "menu_change"))

            self.grid_rowconfigure(0, weight='1') #selection
            self.grid_rowconfigure(1, weight='1') #information
            self.grid_columnconfigure(0, weight='1')

            self.grid(row=0, column=0, sticky="nsew")
            self.grid(row=1, column=0, sticky="nsew")   

    class InformationFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            self.plant_description = self.create_label(text="plant description", row=0, col=0)
            self.plant_water = self.create_label(text="plant water", row=1, col=0)
            self.plant_nutrients = self.create_label(text="plant nutrients", row=2, col=0)   

            self.grid_rowconfigure(0, weight='1') #description
            self.grid_rowconfigure(1, weight='1') #water info
            self.grid_rowconfigure(2, weight='1') #nutrients info
            self.grid_columnconfigure(0, weight='1')