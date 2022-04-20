# Interface and Config
from Interfaces.View_Interface import View
from Interfaces.Sub_Interfaces import Frame, Event
from Methods.config import DEV_CONFIG

# Tkinter
import os
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import StringVar, ttk

class Frame(Frame):
    def __init__(self, master, row, col, border=False):
        super().__init__(master)
        # Define master
        self.master = master

        # Create small black border around frame
        if border:
            self.configure(highlightbackground="black", highlightthickness=1)

        # Default grid layout sticky, put in row/col
        self.grid(stick="nsew", row=row, column=col)

    def create_button(self, text, row, col, event, border=False, color='gray', font_size=12, fill=False):
        # Create new button and configure grid layout
        button = tk.Button(master=self, text=text, command=lambda: self.master.action_performed(event), width=1)
        button.grid(row=row, column=col)

        # Customize button fill, border, and font
        if fill:
            button.grid(sticky="nsew")
        if border:
            button['highlightbackground'] = color
            button['highlightthickness'] = '0.75'
            button['bg'] = color
        button['font'] = f'Arial, {font_size}'

        return button

    def create_label(self, text, row, col):
        # Create new label
        label = ttk.Label(master=self, text=text)

        # Configure label grid layout
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_menu(self, row, col, default, options, event):
        # Create new option menu
        menu = ttk.OptionMenu(self, default, default.get(), *(options), command=lambda x: self.master.action_performed(event))

        # Configure menu grid layout
        menu.rowconfigure(0, weight=1)
        menu.columnconfigure(0, weight=1)
        menu.grid(row=row, column=col)

        return menu

    def create_img(self, row, col, width, height, img_file):
        # Create new PIL image
        img = Image.open((os.path.join(DEV_CONFIG['assets_folder'], img_file)))
        img = img.resize((width, height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # Create new label and add image to label
        label = ttk.Label(self, image=img)
        label.image = img

        # Configure label grid layout
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_button_table(self, row, col, table):
        # Create new frame for table
        table_frame = Frame(master=self, row=row, col=col, border=False)

        # Configure table frame grid layout
        table_frame.grid_columnconfigure(0, weight = 0)

        # Add new label or button for each index of table
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                # First row (x labels)
                if i == 0:
                    # Configure each table frame row
                    table_frame.grid_columnconfigure(j, weight='1')

                    # Skip 0,0
                    if j == 0:
                        continue

                    # Add and Configure each label grid layout
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j)

                # First column (y labels)
                elif j == 0:
                    # Add and Configure each label grid layout
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j, padx='3', ipadx='5')

                # Inactive button (gray)
                elif cell == 0:
                    # Create button with event ("x-label,y-label")
                    b = table_frame.create_button("", i, j, Event("Schedule", f"{table[i][0]},{table[0][j]}"), border=True, fill=True)

                # Scheduled button (green)
                elif cell == 1:
                    # Create button with event ("x-label,y-label")
                    b = table_frame.create_button(j - 1, i, j, Event("Schedule", f"{table[i][0]},{table[0][j]}"), border=True, color='green', fill=True)

                # Active button (blue)
                elif cell == 2:
                    # Create button with event ("active")
                    b = table_frame.create_button(j - 1, i, j, Event("Schedule", f"{table[i][0]},{table[0][j]}"), border=True, color='blue', fill=True)

            # Configure each table frame row grid layout
            table_frame.grid_rowconfigure(i, weight=1)

        return table_frame

    def action_performed(self, e) -> None:
        # Default action is to pass action to master
        self.master.action_performed(e)

class Event(Event):
    def __init__(self, source, event):
        self.source_str = source
        self.event_str = event

    def source(self):
        return self.source_str

    def event(self):
        return self.event_str
    
    def __repr__(self) -> str:
        # Define string rep as "Source: event"
        return f"{self.source}: {self.event}"
        
class View(View):
    def __init__(self, master):
        super().__init__(master)
        
        # Declare controller and define grid sticky layout
        self.controller : object
        self.grid(sticky="nsew",row=0, column=0)

    def create_view(self, schedule, current_plant, plant_types, education_modules):

        # TTK Notebook for tabs
        tabControl = ttk.Notebook(self)

        # Scheduling/watering controls
        self.control_tab = ControlFrame(self, tabControl, schedule, row=0, col=0)
        # Plant selection/information
        self.plant_info_tab = PlantInfoFrame(self, tabControl, current_plant, plant_types, row=0, col=0) 
        # Education modules
        self.education_tab = EducationFrame(self, tabControl, education_modules, row=0, col=0)

        # Add frames to tabs
        tabControl.add(self.control_tab, text ='Controls')
        tabControl.add(self.plant_info_tab, text ='Plant Info')
        tabControl.add(self.education_tab, text ='Education')
        tabControl.pack(expand = 1, fill='both')

    def register_observer(self, observer):
        self.controller = observer

    def set_plant_types(self, types):
        self.plant_types = types
        
    def update_controls(self, schedule, current_time, water_level):
        # Set new schedule
        self.control_tab.schedule = schedule
        self.control_tab.current_time = current_time
        self.control_tab.water_level = water_level

        self.control_tab.water_level_frame.water_label.config(text=f"Water level: {water_level}")

        # Destroy current schedule
        for child in self.control_tab.schedule_frame.winfo_children():
            child.destroy()

        # Create new schedule
        self.control_tab.schedule_frame = self.control_tab.ScheduleFrame(master=self.control_tab, row=1, col=0)

    def update_plant_info(self, type, description, water, nutrients, img_file):
        # Set plant menu var for dropdown menu
        self.plant_info_tab.plant_menu_var.set(type)

        # Set text to match plant menu var
        self.plant_info_tab.information_frame.plant_description.config(text=description)
        self.plant_info_tab.information_frame.plant_water.config(text=water)
        self.plant_info_tab.information_frame.plant_nutrients.config(text=nutrients)

        # Destroy image
        for child in self.plant_info_tab.selection_frame.plant_img_frame.winfo_children():
            child.destroy()

        # Create new image
        self.plant_info_tab.selection_frame.plant_img_frame.create_img(row=0, col=0, width=250, height=250, img_file=img_file)

    def update_education_modules(self, modules):
        # Set modules
        self.education_tab.modules = modules

        # Destroy modules (contains images, so setting only text would leave old images)
        for child in self.education_tab.information_frame.winfo_children():
            child.destroy()

        # Create new modules
        self.education_tab.information_frame = self.education_tab.InformationFrame(self.education_tab, 0, 0)
class ControlFrame(Frame):
    def __init__(self, root, master, schedule, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
        # Define root for access to controller
        self.root = root
        # Define schedule for schedule frame
        self.schedule = schedule
        self.current_time = (0,0)
        self.water_level = 0

        # Water level label
        self.water_level_frame = self.WaterLevelFrame(master=self, row=0, col=0)

        # Schedule 
        self.schedule_frame = self.ScheduleFrame(master=self, row=1, col=0)

        # Control buttons
        self.controls_frame = self.ButtonsFrame(master=self, row=2, col=0)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1) # water level
        self.grid_rowconfigure(1, weight=3) # schedule
        self.grid_rowconfigure(2, weight=1) # control buttons
        self.grid_columnconfigure(0, weight=1)
        self.grid(row= 0, column =0, sticky="nsew")

    def action_performed(self, e):
        # Events from control buttons
        if e.source() == 'Control':
            if e.event() == 'pump_on': # turn on pump manually
                self.root.controller.process_turn_on_pump_event(manual=True)
            if e.event() == 'pump_off': # turn of pump manually
                self.root.controller.process_turn_off_pump_event(manual=True)
            elif e.event() == 'clear_schedule': # clear schedule
                self.root.controller.process_clear_schedule_event()
            elif e.event() == 'load_default_schedule': # load default schedule for plant
                self.root.controller.process_load_plant_default_schedule_event()
            elif e.event() == 'load_custom_schedule': # load custom schedule for plant
                self.root.controller.process_load_plant_custom_schedule_event()
            elif e.event() == 'save_custom_schedule': # save custom schedule for plant
                self.root.controller.process_save_plant_custom_schedule_event()

        # Events from schedule
        elif e.source() == 'Schedule':
            self.root.controller.process_schedule_change_event(e.event())

    class WaterLevelFrame(Frame):
        def __init__(self, master, row=0, col=0, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master
            
            self.water_label = self.create_label(text=f"Water level: {self.master.water_level}", row=0, col=0)

            self.grid_columnconfigure(0, weight='1')
            self.grid_rowconfigure(0, weight='1')

    class ScheduleFrame(Frame): 
        def __init__(self, master, row=0, col=0, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master

            # Title label
            self.title = ttk.Label(self, text="Schedule")
            self.title.grid(row=0)

            # Table of schedule
            self.table = self.create_table_from_schedule(master.schedule, master.current_time)
            self.schedule_frame = self.create_button_table(1, 0, self.table)

            # Configure grid layout
            self.grid_rowconfigure(0, weight=1) #title
            self.grid_rowconfigure(1, weight=12) #table
            self.grid_columnconfigure(0, weight=1)

        def create_table_from_schedule(self, schedule, current_time):
            table = [[0] * 25 for _ in range(7)]
            table.insert(0, [x - 1 for x in range (25)])

            for i, key in enumerate(schedule):
                table[i+1][0] = key
                for x in schedule[key]: 
                    if (key, x) == current_time:
                        table[i+1][x + 1] = 2
                    else:
                        table[i+1][x + 1] = 1

            return table

    class ButtonsFrame(Frame):
        def __init__(self, master, row=0, col=0, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master

            # Load default button
            self.load_default_button = self.create_button(text="Load Default Schedule", row=0, col=0, event=Event("Control", "load_default_schedule"))
            self.load_default_button.config(width='20')
            self.load_default_button.grid_rowconfigure(0, weight='1')

            # Clear button
            self.clear_button = self.create_button(text="Clear Schedule", row=1, col=0, event=Event("Control", "clear_schedule"))
            self.clear_button.config(width='20')
            self.clear_button.grid_rowconfigure(0, weight='1')

            # Load custom button
            self.load_custom_button = self.create_button(text="Load Custom Schedule", row=0, col=2, event=Event("Control", "load_custom_schedule"))
            self.load_custom_button.config(width='20')
            self.load_custom_button.grid_rowconfigure(0, weight='1')

            # Save custom button
            self.load_custom_button = self.create_button(text="Save Custom Schedule", row=1, col=2, event=Event("Control", "save_custom_schedule"))
            self.load_custom_button.config(width='20')
            self.load_custom_button.grid_rowconfigure(0, weight='1')

            # Pump on button
            self.water_button = self.create_button(text="Turn On Pump", row=0, col=1, event=Event("Control", "pump_on"))
            self.water_button.config(width='20')
            self.water_button.grid_rowconfigure(0, weight='1')

            # Pump off button
            self.water_button = self.create_button(text="Turn Off Pump", row=1, col=1, event=Event("Control", "pump_off"))
            self.water_button.config(width='20')
            self.water_button.grid_rowconfigure(0, weight='1')

            # Configure grid layout
            self.grid_columnconfigure(0, weight='1') # clear
            self.grid_columnconfigure(1, weight='1') # water
            self.grid_columnconfigure(2, weight='1') # load
            # self.grid_rowconfigure(0, weight='1')

class PlantInfoFrame(Frame):
    def __init__(self, root, master, plant_menu_var, plant_types, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
        # Define root for access to controller
        self.root = root

        # Define and set plant menu var for default of dropdown menu
        self.plant_menu_var = StringVar(self)
        self.plant_menu_var.set(plant_menu_var)
        # Define plant types for options of dropdown menu
        self.plant_types = plant_types

        # Plant selection 
        self.selection_frame = self.SelectionFrame(self, row=0, col=0)

        # Plant information
        self.information_frame = self.InformationFrame(self, row=0, col=1)

        # Configure grid layout
        self.grid_columnconfigure(0, weight='1') # selection
        self.grid_columnconfigure(1, weight='1') # information
        self.grid_rowconfigure(0, weight='1')
        self.grid_propagate(False)

    def action_performed(self, e):
        # Events from plant selection
        if e.source() == 'Selection':
            if e.event() == 'menu_change':
                self.root.controller.process_menu_change_event(self.plant_menu_var.get())

    class SelectionFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master

            # Image
            self.plant_img_frame = Frame(self, 0, 0)
            self.plant_img = self.plant_img_frame.create_img(row=0, col=0, width=300, height=300, img_file="default.jpg")
            # Configure image grid layout
            self.plant_img_frame.grid_columnconfigure(0, weight='1')
            self.plant_img_frame.grid_rowconfigure(0, weight='1')

            # Dropdown menu
            self.plant_dropdown = self.create_menu(row=1, col=0, default=master.plant_menu_var, options=master.plant_types, event=Event("Selection", "menu_change"))

            # Configure grid layout
            self.grid_rowconfigure(0, weight='1') # selection
            self.grid_rowconfigure(1, weight='1') # information
            self.grid_columnconfigure(0, weight='1')

    class InformationFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master

            # Text labels
            self.plant_description = self.create_label(text="plant description", row=0, col=0)
            self.plant_water = self.create_label(text="plant water", row=1, col=0)
            self.plant_nutrients = self.create_label(text="plant nutrients", row=2, col=0)   
            
            # Configure text wrap length
            self.plant_description.configure(wraplength=300)
            self.plant_water.configure(wraplength=300)
            self.plant_nutrients.configure(wraplength=300)

            # Configure grid layout
            self.grid_rowconfigure(0, weight='1') # description
            self.grid_rowconfigure(1, weight='1') # water info
            self.grid_rowconfigure(2, weight='1') # nutrients info
            self.grid_columnconfigure(0, weight='1')

class EducationFrame(Frame):
    def __init__(self, root, master, modules, row=0, col=0, border=False):
        super().__init__(master, row=row, col=col, border=border)
        # Define root for access to controller
        self.root = root

        # Set modules
        self.modules = modules

        # Information frame
        self.information_frame = self.InformationFrame(self, 0, 0)

        # Configure grid layout
        self.grid_columnconfigure(0, weight='1')

    class InformationFrame(Frame):
        def __init__(self, master, row, col, border=False):
            super().__init__(master, row=row, col=col, border=border)
            # Define master for access to data and action
            self.master = master

            # Create scrollable canvas
            canvas = tk.Canvas(self)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            # Configure scrollable
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all"),
                    height=500
                )
            )

            # Configure canvas
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # New frame with image, title, and text for each module
            for i, module in enumerate(master.modules):
                module_name = module

                # Get module data (text and image)
                module = master.modules[module]

                # Create new frame
                module_frame = Frame(scrollable_frame, i, 0)
                text_frame = Frame(scrollable_frame, i, 1)

                # Get text and image from module
                text = module["text"]
                img_file = module["img_file"]

                # Create new image and label
                img = module_frame.create_img(row = 0, col=0, width=150, height=100, img_file=img_file)
                title = text_frame.create_label(module_name, row=0, col=0)
                text = text_frame.create_label(text=text, row=1, col=0) 

                # Configure text wrap length
                text.configure(wraplength=600)

                # Configure text frame grid layout
                text_frame.grid_rowconfigure(0, weight='1')
                text_frame.grid_rowconfigure(1, weight='3')
                text_frame.grid_columnconfigure(0, weight='1')

                # Configure module frame grid layout
                module_frame.grid_columnconfigure(0, weight='1')
                module_frame.grid_columnconfigure(1, weight='2')
                module_frame.grid_rowconfigure(0, weight='1')

                # Configure padding between modules
                module_frame.configure(pady='20')

                # Configure each row grid layout
                scrollable_frame.grid_rowconfigure(i, weight='1')

            # Configure pack layout
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
