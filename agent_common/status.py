

from sense_hat import SenseHat
from database.models import Scooter


class Status:

    def __init__(self, scooter_id:int) -> None:
        self.sense = SenseHat()
        self.status = ''
        self.scooter_id = scooter_id

    def get_status(self):
        '''
        get scooter status from database
        '''
        pass


    def display_status(self):
        '''
        display the color representation of the status
        '''
        pass

