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
    def set_contoller():
        pass

    @abstractclassmethod
    def event_handler():
        pass

    @abstractclassmethod
    def set_plant_types():
        pass

    @abstractclassmethod
    def set_plant_info():
        pass

    @abstractclassmethod
    def set_schedule():
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

        self.control_tab = ControlFrame(schedule, master=tabControl, row=0, col=0, weight=1)
        self.information_tab = ttk.Frame(tabControl)
        self.education_tab = ttk.Frame(tabControl)

        tabControl.add(self.control_tab, text ='Controls')
        tabControl.add(self.information_tab, text ='Plant Info')
        tabControl.add(self.education_tab, text ='Education')
        tabControl.pack(expand = 1, fill ="both")

    def set_contoller(self, controller):
        self.controller = controller

    def set_plant_types(self, types):
        self.plant_types = types
        
    def set_schedule(self, schedule):
        self.control_tab.schedule = schedule

    def set_plant_info(self, type, description, water, nutrients, img_file):
        top_right_frame = self.top_frame.top_right_frame

        self.plant_menu_var.set(type)
        top_right_frame.information_frame.plant_description.config(text=description)
        top_right_frame.information_frame.plant_water.config(text=water)
        top_right_frame.information_frame.plant_nutrients.config(text=nutrients)
        top_right_frame.selection_frame.create_img(row=1, col=0, width=150, height=150, img_file=img_file)

    def event_handler(self, event=''):
        if event == 'left clicked':
            water_level = int(self.water_label['text'].split()[2]) + 10
            self.top_left_frame.water_label.config(text=f'Water level: {water_level}')
            print(water_level)

        elif event == 'right clicked':
            print(self.plant_types)

        elif event == 'plant_menu':
            self.controller.update_plant_type(self.plant_menu_var.get())

        self.controller.update_view_to_match_model()

class ControlFrame(Frame):
    def __init__(self, schedule, master, row=0, col=0, weight=1):
        super().__init__(master, row=row, col=col, border=True)

        self.schedule = schedule

        #widgets
        self.water_label = self.create_label(text="Water level: 100", row=0, col=0)
        self.schedule_frame = ScheduleFrame(master=self, row=1, col=0)
        self.water_button = self.create_button(text="Water Now", row=2, col=0, event='water_now')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def actionPerformed(self, e):
        pass
    
class PlantInfoFrame(Frame):
    def __init__(self, master, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, row=row, col=col, border=True)

        self.selection_frame = SelectionFrame(self, num_rows=3, row=0, col=0)
        self.information_frame = InformationFrame(self, num_rows=3, row=1, col=0, weight = 10)

class SelectionFrame(Frame):
    def __init__(self, master, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, row=row, col=col, border=True)

        self.plant_img = self.create_img(1, 0, 50, 50, "default.jpg")
        self.root.plant_menu_var.set('select plant')
        self.root.plant_dropdown = self.create_menu(2, 0, self.root.plant_menu_var, self.root.plant_types, 'plant_menu')
        
class InformationFrame(Frame):
    def __init__(self, master, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, row=row, col=col, border=True)

        #widgets
        self.plant_description = self.create_label("plant description", 0, 0)
        self.plant_water = self.create_label("plant water", 1, 0)
        self.plant_nutrients = self.create_label("plant nutrients", 2, 0)   

class ScheduleFrame(Frame): 
    def __init__(self, master, row=0, col=0):
        super().__init__(master, row=row, col=col, border=False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)
        self.grid_columnconfigure(0, weight=1)

        self.title = ttk.Label(self, text="Schedule")
        self.title.grid(row=0)
        self.table = self.update_table_from_schedule(master.schedule)
        self.schedule_frame = self.create_button_table(1, 0, self.table)

    def update_table_from_schedule(self, schedule):
        table = [[0] * 25 for _ in range(7)]
        table.insert(0, [x - 1 for x in range (25)])

        for i, key in enumerate(schedule):
            table[i+1][0] = key
            for x in schedule[key]: table[i+1][x + 1] = 1

        return table

    def actionPerformed(self, e):
        day, time = e.split(",")
        time = int(time)
        day_schedule = self.master.schedule[day]

        if time not in day_schedule:
            day_schedule.append(time)
        else:
            day_schedule = [x for x in day_schedule if x != time]
            
        self.master.schedule[day] = day_schedule
        self = ScheduleFrame(master=self.master, row=1, col=0)

        
