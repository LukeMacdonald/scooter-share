

from sense_hat import SenseHat
from database.models import Scooter
from database.database_manager import db


class Status:

    def __init__(self, scooter_id:int, db) -> None:
        self.sense = SenseHat()
        self.scooter_id = scooter_id
        self.session = db.session

    def get_status(self):
        '''
        get scooter status from database
        '''

        # I'm not all too sure how SQLAlchemy works gotta get this checked
        self.status = self.session.query(Scooter.status).filter_by(id=self.scooter_id).first()
        


    def display_status(self):
        '''
        display the color representation of the status
        '''
        if self.status == 'available':
            self.sense.clear((0, 255, 0))
        elif self.status == 'occupying':
            self.sense.clear((255, 0, 0))
        elif self.status == 'awaiting repair':
            self.sense.clear((170, 100, 20))
        else:
            self.sense.clear()


if __name__ == '__main__':
    status = Status(0, db)