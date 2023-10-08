

from sense_hat import SenseHat
from agent.web.connection import get_connection

class Status:

    def __init__(self, scooter_id:int) -> None:
        self.sense = SenseHat()
        self.scooter_id = scooter_id
        self.get_status()
        self.display_status()


    def update_local_status(self):
        self.get_status()
        self.display_status()
        
    def get_status(self):
        '''
            get scooter status from database
        '''

        response = get_connection().send({'scooter_id': self.scooter_id, 'name': 'get-scooter-by-id'})
        self.status = response['status']

    def display_status(self):
        '''
            display the color representation of the status
        '''
        if self.status == 'available':
            self.sense.clear((0, 255, 0))
        elif self.status == 'occupying':
            self.sense.clear((0, 125, 200))
        elif self.status == 'awaiting repair':
            self.sense.clear((170, 100, 20))
        else:
            self.sense.clear()

