from abc import ABC, abstractclassmethod

class Model(ABC):
    '''Model for HydroponiKs'''
    @abstractclassmethod
    def set_plant_type(self, type:str) -> None:
        '''Set current plant type selected'''

    @abstractclassmethod
    def set_schedule(self, schedule: dict) -> None:
        '''Set model schedule to schedule'''

    @abstractclassmethod
    def set_plant_custom_schedule(self) -> None:
        '''Set current plant custom schedule to current schedule'''
        
    @abstractclassmethod
    def set_pump_active_status(self, status: bool) -> None:
        '''Set active status of pump (True/False == On/Off)'''

    @abstractclassmethod
    def set_manual_override_status(self, status: bool) -> None:
        '''Set status of manual override'''

    @abstractclassmethod
    def set_pump_status(self, status: int) -> None:
        '''Set strength of pump on arduino'''

    @abstractclassmethod
    def get_time(self) -> tuple:
        '''Return current (day,time)'''

    @abstractclassmethod
    def get_pump_active_status(self) -> bool:
        '''Retrun current active status of pump (True/False == On/Off)''' 

    @abstractclassmethod
    def get_manual_override_status(self) -> bool:
        '''Return status of manual override'''  

    @abstractclassmethod
    def get_plant_description(self) -> str:
        '''Return current plant's description'''
    
    @abstractclassmethod
    def get_plant_type(self) -> str:
        '''Return current plant type'''

    @abstractclassmethod
    def get_plant_water(self) -> str:
        '''Return current plant's water needs'''
        
    @abstractclassmethod
    def get_plant_nutrients(self) -> str:
        '''Return current plant's nutrients needs'''
        
    @abstractclassmethod
    def get_plant_img_file(self) -> str:
        '''Return current plant's image file name'''
        
    @abstractclassmethod
    def get_plant_default_schedule(self) -> dict:
        '''Return current plant's default schedule dictionary'''
        
    @abstractclassmethod
    def get_plant_custom_schedule(self) -> dict:
        '''Return current plant's custom schedule dictionary'''
        
    @abstractclassmethod
    def get_plant_types(self) -> list:
        '''Return list of all plant types'''
        
    @abstractclassmethod
    def get_schedule(self) -> dict:
        '''Return current schedule dictionary'''
        
    @abstractclassmethod
    def get_education_modules(self) -> dict:
        '''Return the dictionary of education modules'''

    @abstractclassmethod
    def get_water_level(self) -> str:
        '''Return water level from arduino'''

    @abstractclassmethod
    def update_water_level(self) -> None:
        '''Update water level from arduino'''
        
    @abstractclassmethod
    def load_plants(self) -> None:
        '''Load names of plant types'''
        
    @abstractclassmethod
    def load_education_modules(self) -> None:
        '''Load education modules containing text and images'''
     
    @abstractclassmethod
    def load_save_state(self) -> None:
        '''Load save state of schedule/plant type from json'''
        
    @abstractclassmethod
    def dump_save_state(self) -> None:
        '''Dump save state of schedule/plant type to json''' 