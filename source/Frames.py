import tkinter as tk
from tkinter import ttk, StringVar
from abc import ABC, abstractclassmethod
from PIL import ImageTk, Image
import os

class Frame(ABC, tk.Frame):
    @abstractclassmethod
    def create_button() -> tk.Label:
        pass

    @abstractclassmethod
    def create_label() -> ttk.Label:
        pass

    @abstractclassmethod
    def create_menu() -> ttk.OptionMenu:
        pass

    @abstractclassmethod
    def create_img() -> ttk.Label:
        pass

    @abstractclassmethod
    def create_button_table() -> tk.Frame:
        pass

class Frame(Frame):
    '''Generic Frame'''
    def __init__(self, master, row, col, border=False):
        super().__init__(master)
        self.master = master

        if border:
            self.configure(highlightbackground="black", highlightthickness=1)

        self.grid(stick="nsew", row=row, column=col)

    def create_button(self, text: str, row: int, col: int, event: str, border=False, color='gray', font_size=12, fill=False) -> None:
        '''Return new button'''

        button = tk.Button(master=self, text=text, command=lambda: self.master.action_performed(event), width=1, padx=1)
        #button = tkm.Button(master=self, text=text, command=lambda: self.root.event_handler(event))
        button.grid(row=row, column=col)

        if fill:
            button.grid(sticky="nsew")

        if border:
            button['highlightbackground'] = color
            button['highlightthickness'] = '0.5'

        button['font'] = f'Arial, {font_size}'

        return button

    def create_label(self, text: str, row: int, col: int):
        '''Return new label'''
        label = ttk.Label(master=self, text=text)
        label.rowconfigure(0, weight=1)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=col)

        return label

    def create_menu(self, row: int, col: int, default: StringVar, options: list, event: str):
        '''Return new options menu'''
        menu = ttk.OptionMenu(self, default, default.get(), *(options), command=lambda: self.master.action_performed(event))
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

    def create_button_table(self, row: int, col: int, table: list):
        table_frame = Frame(master=self, row=row, col=col, border=False)
        table_frame.grid_columnconfigure(0, weight = 0)
        buttons = []

        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                if i == 0:
                    table_frame.grid_columnconfigure(i, weight=1)
                    if cell == -1:
                        continue
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j)

                elif cell == 1:
                    b = table_frame.create_button(j - 1, i, j, f"{table[i][0]},{j - 1}", border=True, color='green', fill=True)

                elif cell == 0:
                    b = table_frame.create_button("", i, j, f"{table[i][0]},{j - 1}", border=True, fill=True)

                else:
                    b = ttk.Label(table_frame, text=str(cell))
                    b.grid(row=i, column=j)

                buttons.append(b)
            
            table_frame.grid_rowconfigure(i, weight=1)

        return table_frame
            