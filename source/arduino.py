import os
import json_methods
from pyfirmata import Arduino, util

ARDUINO_CONFIG_FILE_PATH = os.path.join('config', 'arduino-config.json')
ARDUINO_CONFIG = json_methods.load_json(ARDUINO_CONFIG_FILE_PATH)

class Arduino(Arduino):
    def __init__(self):
        #try connecting to serial monitor
        try:

            active = ARDUINO_CONFIG['active']
            if active == "FALSE":
                self.active = False
            elif active == "TRUE":
                self.active = True
            else:
                raise self.ArduinoException("Invalid Arduino Active Status")

            if not self.active:
                raise self.ArduinoException("Arduino Inactive")

            self.board = Arduino(ARDUINO_CONFIG['com_port'])

            it = util.Iterator(self.board)
            it.start()

            self.water_level_pin = self.board.get_pin(ARDUINO_CONFIG['water_level_pin'])
            self.pump_pin= self.board.get_pin(ARDUINO_CONFIG['pump_pin'])

            self.active = True
            print("Connected successfully!")

        except self.ArduinoException as error:
            print(f"Connecting unsuccesful: {error}")
            print("Proceeding without connection...")
            self.active = False

        except Exception as error:
            print(f"Error: {error}")
            print("Connection unsuccessful. Quitting...")
            quit()

    def write_to_pin(pin, val):
        pin.write(val)

    def read_from_pin(self, pin):
        val = pin.read()
        return val

    class ArduinoException(Exception):
        pass