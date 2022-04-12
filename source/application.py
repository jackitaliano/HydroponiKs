import tkinter as tk
from view import View
from model import Model
from controller import Controller1
import atexit

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        #window width
        window_width = 15 * screen_width // 24
        window_height = 15 * screen_height // 24

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.title("HydroponiKs")
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.model = Model()
        self.view = View(self)

        self.view.create_view(self.model.get_schedule())

        self.controller = Controller1(self.model, self.view)

        self.view.set_contoller(self.controller)

        self.mainloop()


if __name__ == '__main__':
    app = App()

    atexit.register(app.model.save_state)