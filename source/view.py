from abc import ABC, abstractclassmethod
import os
import tkinter as tk
from tkinter import StringVar, ttk
import tkmacosx as tkm
from PIL import ImageTk, Image

class View(tk.Frame, ABC):
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

class Frame(tk.Frame, ABC):
    @abstractclassmethod
    def create_button():
        pass

    @abstractclassmethod
    def create_label():
        pass

    @abstractclassmethod
    def create_menu():
        pass

    @abstractclassmethod
    def create_img():
        pass

    @abstractclassmethod
    def create_button_table():
        pass

class View1(View):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.controller : object

        self.master = master
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="nsew",row=0, column=0)

        self.plant_types : list
        self.schedule : dict
        self.plant_menu_var = tk.StringVar(self)

        #self.create_view()

    def create_view(self):
        #TOP frame
        self.top_frame = TopFrame(master=self, root=self, num_cols=2, row=0, col=0, weight=1)

        ##BOTTOM frame
        self.bottomFrame = BottomFrame(master=self, root=self, row=1, col=0, weight=1)

    def set_contoller(self, controller):
        self.controller = controller

    def set_plant_types(self, types):
        self.plant_types = types

    def set_schedule(self, schedule):
        self.schedule = schedule

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

class Frame1(Frame):
    '''Generic Frame'''
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1, border=False):
        super().__init__(master)
        self.master = master
        self.root = root
        self.grid_propagate(False)

        if border:
            self.configure(highlightbackground="black", highlightthickness=1)

        for i in range(num_rows):
            self.grid_rowconfigure(i, weight=weight)
        
        for i in range(num_cols):
            self.grid_columnconfigure(i, weight=weight)
        self.grid(stick="nsew", row=row, column=col)

    def create_button(self, text : str, row : int, col : int, event : str, border=False, color='gray', font_size=12, fill=False) -> None:
        '''Return new button'''

        button = tk.Button(master=self, text=text, command=lambda: self.root.event_handler(event), width=1, padx=0)
        #button = tkm.Button(master=self, text=text, command=lambda: self.root.event_handler(event))
        button.grid(row=row, column=col)

        if fill:
            button.grid(sticky=tk.N+tk.E+tk.S+tk.W)

        if border:
            button['highlightbackground'] = color
            button['highlightthickness'] = '0.5'

        button['font'] = f'Arial, {font_size}'
        # button['padx'] = 0
        # button['pady'] = 0

        return button

    def create_label(self, text: str, row: int, col: int):
        '''Return new label'''
        label = ttk.Label(master=self, text=text)
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_menu(self, row : int, col : int, default : StringVar, options : list, event : str):
        '''Return new options menu'''
        menu = ttk.OptionMenu(self, default, default.get(), *(options), command=lambda x:self.root.event_handler(event))
        menu.rowconfigure(0, weight=1)
        menu.columnconfigure(0, weight=1)
        menu.grid(row=row, column=col)

        return menu

    def create_img(self, row: int, col: int, width: int, height: int, img_file: str):
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

    def create_button_table(self, num_rows, num_cols, row, col, table):
        table_frame = Frame1(master=self, root=self.root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, border=True)
        table_frame.grid_columnconfigure(0, weight = 0)
        buttons = []

        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                if i == 0:
                    if cell == -1:
                        continue
                    b = ttk.Label(table_frame, text=str(cell))

                elif cell == 1:
                    b = table_frame.create_button("", i, j, "", border=True, color='green', font_size=5, fill=True)

                elif cell == 0:
                    b = table_frame.create_button("", i, j, "", border=True, fill=True)

                else:
                    b = ttk.Label(table_frame, text=str(cell))

                table_frame.grid_columnconfigure(j, weight = 0)
                buttons.append(b)

        return table_frame

class TopFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight, border=True)
        
        #TOP LEFT frame
        self.top_left_frame = TopLeftFrame(master=self, root=root, num_rows=3, row=0, col=0)
        self.top_left_frame.grid_rowconfigure(0, weight=1)
        self.top_left_frame.grid_rowconfigure(1, weight=3)
        self.top_left_frame.grid_rowconfigure(2, weight=1)

        #TOP RIGHT frame
        self.top_right_frame = TopRightFrame(master=self, root=root, num_rows=2, row=0, col=1)
        self.top_right_frame.grid_rowconfigure(0, weight=1)
        self.top_right_frame.grid_rowconfigure(1, weight=2)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)


class TopLeftFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight, border=True)

        #widgets
        self.water_label = self.create_label("Water level: 100", 0, 0)
        self.schedule_frame = ScheduleFrame(master=self, root=root, num_rows=2, num_cols=1, row=1, col=0)
        self.water_button = self.create_button("Water Now", 2, 0, 'water_now')
        
class TopRightFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight, border=True)

        self.selection_frame = SelectionFrame(self, root, num_rows=3, row=0, col=0)
        self.information_frame = InformationFrame(self, root, num_rows=3, row=1, col=0, weight = 10)
    
class BottomFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight)

        #widgets
        self.create_button("bottom", 0, 0, 'bottom clicked')

class SelectionFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight)

        self.plant_img = self.create_img(1, 0, 50, 50, "default.jpg")
        self.root.plant_menu_var.set('select plant')
        self.root.plant_dropdown = self.create_menu(2, 0, self.root.plant_menu_var, self.root.plant_types, 'plant_menu')
        
class InformationFrame(Frame1):
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight)

        #widgets
        self.plant_description = self.create_label("plant description", 0, 0)
        self.plant_water = self.create_label("plant water", 1, 0)
        self.plant_nutrients = self.create_label("plant nutrients", 2, 0)   

class ScheduleFrame(Frame1): 
    def __init__(self, master, root, num_rows=1, num_cols=1, row=0, col=0, weight=1):
        super().__init__(master, root, num_rows=num_rows, num_cols=num_cols, row=row, col=col, weight=weight)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=12)

        self.title = ttk.Label(self, text="Schedule")
        self.title.grid(row=0)
        self.table = self.get_table_from_schedule(self.root.schedule)
        self.schedule_frame = self.create_button_table(9, 25, 1, 0, self.table)

    def get_table_from_schedule(self, schedule):
        table = [[0] * 25 for _ in range(7)]
        table.insert(0, [x - 1 for x in range (25)])

        for i, key in enumerate(schedule):
            table[i+1][0] = key
            for x in schedule[key]: table[i+1][x] = 1

        return table

        
