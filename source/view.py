from abc import ABC, abstractclassmethod
import os
import tkinter as tk
from tkinter import StringVar, ttk
import tkmacosx as tkm
from Frames import Frame

class View(ABC, tk.Frame):
    @abstractclassmethod
    def create_view():
        pass

    @abstractclassmethod
    def register_observer():
        pass

    @abstractclassmethod
    def action_performed():
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

        self.plant_types : list
        self.plant_menu_var = tk.StringVar(self)

    def create_view(self, schedule):

        tabControl = ttk.Notebook(self)

        self.control_tab = ControlFrame(self, tabControl, schedule, row=0, col=0, weight=1)
        self.plant_info_tab = PlantInfoFrame(master=tabControl, row=0, col=0, weight=1)
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

    def update_plant_info(self, type, description, water, nutrients, img_file):
        top_right_frame = self.top_frame.top_right_frame

        self.plant_menu_var.set(type)
        top_right_frame.information_frame.plant_description.config(text=description)
        top_right_frame.information_frame.plant_water.config(text=water)
        top_right_frame.information_frame.plant_nutrients.config(text=nutrients)
        top_right_frame.selection_frame.create_img(row=1, col=0, width=150, height=150, img_file=img_file)

    def action_performed(self, event):
        pass

        self.controller.update_view_to_match_model()
class Event():
    def __init__(self, source, event):
        self.source = source
        self.event = event
class ControlFrame(Frame):
    def __init__(self, root, master, schedule, row=0, col=0, weight=1):
        super().__init__(master, row=row, col=col, border=True)

        self.root = root
        self.schedule = schedule

        #water level label
        self.water_label = self.create_label(text="Water level: 100", row=0, col=0)

        #schedule 
        self.schedule_frame = ScheduleFrame(master=self, row=1, col=0)

        #frame containing water now button
        self.water_now_frame = Frame(self, 2, 0)
        self.water_now_frame.grid_columnconfigure(0, weight='1')

        #water button
        self.water_button = self.water_now_frame.create_button(text="Water Now", row=0, col=0, event='water_now')
        self.water_button.config(width='20')
        self.water_button.grid_rowconfigure(0, weight='1')

        self.grid_rowconfigure(0, weight=1) #water level
        self.grid_rowconfigure(1, weight=3) #schedule
        self.grid_rowconfigure(2, weight=1) #water now button
        self.grid_columnconfigure(0, weight=1)
        self.grid(row= 0, column =0, sticky="nsew")

    def update_schedule(self, schedule):
        self.schedule = schedule

    def action_performed(self, e):
        if e == 'water_now':
            self.master.master.controller.process_water_event()

class ScheduleFrame(Frame): 
    def __init__(self, master, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
 
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

    def action_performed(self, e):
        day, time = e.split(",")
        time = int(time)
        day_schedule = self.master.schedule[day]

        if time not in day_schedule:
            day_schedule.append(time)
        else:
            day_schedule = [x for x in day_schedule if x != time]
            
        self.master.schedule[day] = day_schedule
        self = ScheduleFrame(master=self.master, row=1, col=0)
class PlantInfoFrame(Frame):
    def __init__(self, master, row, col, border=False):
        super().__init__(master, row=row, col=col, border=border)

        self.selection_frame = SelectionFrame(self, row=0, col=0)
        self.information_frame = InformationFrame(self, row=0, col=1)
class SelectionFrame(Frame):
    def __init__(self, master, row, col, border=False):
        super().__init__(master, row=row, col=col, border=border)

        self.plant_img = self.create_img(1, 0, 50, 50, "default.jpg")
        self.master.plant_menu_var.set('select plant')
        self.master.plant_dropdown = self.create_menu(row=2, col=0, default=self.root.plant_menu_var, options=self.root.plant_types, event='plant_menu')        
class InformationFrame(Frame):
    def __init__(self, master, row, col, border=False):
        super().__init__(master, row=row, col=col, border=border)

        self.plant_description = self.create_label(text="plant description", row=0, col=0)
        self.plant_water = self.create_label(text="plant water", row=1, col=0)
        self.plant_nutrients = self.create_label(text="plant nutrients", row=2, col=0)   
