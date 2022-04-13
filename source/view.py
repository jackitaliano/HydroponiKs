import os
import tkinter as tk
from tkinter import StringVar, ttk
from PIL import ImageTk, Image
from MVCInterfaces import View, Frame, Event

class Frame(Frame):
    def __init__(self, master, row, col, border=False):
        super().__init__(master)
        self.master = master

        if border:
            self.configure(highlightbackground="black", highlightthickness=1)

        self.grid(stick="nsew", row=row, column=col)

    def create_button(self, text, row, col, event, border=False, color='gray', font_size=12, fill=False):

        button = tk.Button(master=self, text=text, command=lambda: self.master.action_performed(event), width=1)
        button.grid(row=row, column=col)

        if fill:
            button.grid(sticky="nsew")

        if border:
            button['highlightbackground'] = color
            button['highlightthickness'] = '0.5'

        button['font'] = f'Arial, {font_size}'

        return button

    def create_label(self, text, row, col):
        '''Return new label'''
        label = ttk.Label(master=self, text=text)
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_menu(self, row, col, default, options, event):
        '''Return new options menu'''
        menu = ttk.OptionMenu(self, default, default.get(), *(options), command=lambda x: self.master.action_performed(event))
        menu.rowconfigure(0, weight=1)
        menu.columnconfigure(0, weight=1)
        menu.grid(row=row, column=col)

        return menu

    def create_img(self, row, col, width, height, img_file):
        '''Return new image'''
        img = Image.open((os.path.join('assets', img_file)))
        img = img.resize((width, height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label = ttk.Label(self, image=img)
        label.image = img
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_button_table(self, row, col, table):
        table_frame = Frame(master=self, row=row, col=col, border=False)
        table_frame.grid_columnconfigure(0, weight = 0)
        buttons = []

        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                if i == 0:
                    table_frame.grid_columnconfigure(j, weight=1)
                    if cell == -1:
                        continue
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j)

                elif cell == 1:
                    b = table_frame.create_button(j - 1, i, j, Event("Schedule", f"{table[i][0]},{j - 1}"), border=True, color='green', fill=True)

                elif cell == 0:
                    b = table_frame.create_button("", i, j, Event("Schedule", f"{table[i][0]},{j - 1}"), border=True, fill=True)

                else:
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j)
            
            table_frame.grid_rowconfigure(i, weight=1)

        return table_frame

    def action_performed(self, e) -> None:
        self.master.action_performed(e)

class Event(Event):
    def __init__(self, source, event):
        self.source_str = source
        self.event = event

    def source(self):
        return self.source_str
    
    def __repr__(self) -> str:
        return self.event
class View(View):
    def __init__(self, master):
        super().__init__(master)
        
        self.controller : object
        self.grid(sticky="nsew",row=0, column=0)

    def create_view(self, schedule, current_plant, plant_types, education_modules):

        tabControl = ttk.Notebook(self)

        self.control_tab = ControlFrame(self, tabControl, schedule, row=0, col=0)
        self.plant_info_tab = PlantInfoFrame(self, tabControl, current_plant, plant_types, row=0, col=0)
        self.education_tab = EducationFrame(self, tabControl, education_modules, row=0, col=0)

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

        for child in self.plant_info_tab.selection_frame.plant_img_frame.winfo_children():
            child.destroy()
        self.plant_info_tab.selection_frame.plant_img_frame.create_img(row=0, col=0, width=250, height=250, img_file=img_file)

    def update_education_modules(self, modules):
        self.education_tab.modules = modules

        for child in self.education_tab.information_frame.winfo_children():
            child.destroy()
        self.education_tab.information_frame = self.education_tab.InformationFrame(self.education_tab, 0, 0)
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
        self.water_now_frame.grid_columnconfigure(1, weight='1')
        self.water_now_frame.grid_columnconfigure(2, weight='1')

        #clear button
        self.water_button = self.water_now_frame.create_button(text="Clear Schedule", row=0, col=0, event=Event("Control", "clear_schedule"))
        self.water_button.config(width='20')
        self.water_button.grid_rowconfigure(0, weight='1')

        #water button
        self.water_button = self.water_now_frame.create_button(text="Water Now", row=0, col=1, event=Event("Control", "water_now"))
        self.water_button.config(width='20')
        self.water_button.grid_rowconfigure(0, weight='1')

        self.water_button = self.water_now_frame.create_button(text="Load Plant Schedule", row=0, col=2, event=Event("Control", "load_schedule"))
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
            elif str(e) == 'load_schedule':
                self.root.controller.process_load_plant_schedule_event()
            elif str(e) == 'clear_schedule':
                self.root.controller.process_clear_schedule_event()

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
            self.table = self.create_table_from_schedule(master.schedule)
            self.schedule_frame = self.create_button_table(1, 0, self.table)

            self.grid_rowconfigure(0, weight=1) #title
            self.grid_rowconfigure(1, weight=12) #table
            self.grid_columnconfigure(0, weight=1)

        def create_table_from_schedule(self, schedule):
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
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight='1')

    def action_performed(self, e):
        if e.source() == 'Selection':
            if str(e) == 'menu_change':
                self.root.controller.process_menu_change_event(self.plant_menu_var.get())

    class SelectionFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            self.plant_img_frame = Frame(self, 0, 0)
            self.plant_img = self.plant_img_frame.create_img(row=0, col=0, width=300, height=300, img_file="default.jpg")
            self.plant_img_frame.grid_columnconfigure(0, weight='1')
            self.plant_img_frame.grid_rowconfigure(0, weight='1')

            self.plant_dropdown = self.create_menu(row=1, col=0, default=master.plant_menu_var, options=master.plant_types, event=Event("Selection", "menu_change"))

            self.grid_rowconfigure(0, weight='1') #selection
            self.grid_rowconfigure(1, weight='1') #information
            self.grid_columnconfigure(0, weight='1')

    class InformationFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            self.plant_description = self.create_label(text="plant description", row=0, col=0)
            self.plant_water = self.create_label(text="plant water", row=1, col=0)
            self.plant_nutrients = self.create_label(text="plant nutrients", row=2, col=0)   

            self.plant_description.configure(wraplength=300)
            self.plant_water.configure(wraplength=300)
            self.plant_nutrients.configure(wraplength=300)

            self.grid_rowconfigure(0, weight='1') #description
            self.grid_rowconfigure(1, weight='1') #water info
            self.grid_rowconfigure(2, weight='1') #nutrients info
            self.grid_columnconfigure(0, weight='1')

class EducationFrame(Frame):
    def __init__(self, root, master, modules, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)

        self.root = root

        self.modules = modules

        self.information_frame = self.InformationFrame(self, 0, 0)

        self.grid_columnconfigure(0, weight='1')
        
    class InformationFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            self.master = master

            for i, module in enumerate(master.modules):
                module = master.modules[module]
                frame = Frame(self, i, 0)
                text = module["text"]
                img_file = module["img_file"]

                img = frame.create_img(row = 0, col=0, width=100, height=100, img_file=img_file)
                text = frame.create_label(text=text, row=0, col=1) 

                text.configure(wraplength=500)

                frame.grid_columnconfigure(0, weight='1')
                frame.grid_columnconfigure(1, weight='2')
                frame.grid_rowconfigure(0, weight='1')

                self.grid_rowconfigure(i, weight='1')

            self.grid_columnconfigure(0, weight = '1')

