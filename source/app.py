import tkinter as tk
from view import View
from model import Model
from controller import Controller
from config import DEV_CONFIG
import atexit

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define window dimensions
        window_width = 5 * screen_width // 8
        window_height = 5 * screen_height // 8

        # Find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # Configure window
        self.title("HydroponiKs")
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(True, True)
        self.minsize(5 * screen_width // 8, 5 * screen_height // 8)

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

    def update_controller_time_for_schedule(self):
        self.controller.handle_time()

        self.after(DEV_CONFIG['update_time_ms'], self.update_controller_time_for_schedule)


if __name__ == '__main__':
    app = App()

    # Register model exit to exit
    atexit.register(app.controller.exit)