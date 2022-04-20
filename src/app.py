# Interfaces and config
from view import View
from model import Model
from controller import Controller
from Methods.config import DEV_CONFIG

# Tkinter
import tkinter as tk

# On exit command
import atexit

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define window dimensions
        window_width = int(screen_width * DEV_CONFIG['window_default_scale'])
        window_height = int(screen_height * DEV_CONFIG['window_default_scale'])

        min_width = int(screen_width * DEV_CONFIG['window_min_scale'])
        min_height = int(screen_height * DEV_CONFIG['window_min_scale'])

        max_width = int(screen_width * DEV_CONFIG['window_max_scale'])
        max_height = int(screen_height * DEV_CONFIG['window_max_scale'])

        # Find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # Configure window
        self.title(DEV_CONFIG['window_title'])
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(DEV_CONFIG['resizable_x'], DEV_CONFIG['resizable_y'])
        self.minsize(min_width, min_height)
        self.maxsize(max_width, max_height)

        # Configure window grid
        self.grid_rowconfigure(0, weight='1')
        self.grid_columnconfigure(0, weight='1')

        # Define MVC
        self.model = Model()
        self.view = View(self)
        self.controller = Controller(self.model, self.view)

        # Register controller to view
        self.view.register_observer(self.controller)

        # Create and update view
        self.view.create_view(self.model.get_schedule(), self.model.get_plant_type(), self.model.get_plant_types(), self.model.get_education_modules())
        self.controller.update_view_to_match_model() 

        self.after(DEV_CONFIG['update_time_ms'], self.update_controller_time_for_schedule)

        self.mainloop()

    def exit(self):
        self.controller.exit()

    def update_controller_time_for_schedule(self):
        self.controller.handle_time()

        self.after(DEV_CONFIG['update_time_ms'], self.update_controller_time_for_schedule)


if __name__ == '__main__':
    app = App()

    # Register model exit to exit
    atexit.register(app.exit)