from sense_hat import SenseHat
from agent.web.connection import get_connection


class CrashDetection():
    def __init__(self, scooter_id:int) -> None:
        self.scooter_id = scooter_id
        self.in_use = False
        self.sense = SenseHat()
        self.threashold = 5 # Change for detection severity 50 == ~5g probably best.


    def ask_for_repair(self):
        print('Scooter Crashed! Requesting Repair.')
        get_connection().send({
            'scooter_id': self.scooter_id,
            'name': 'request-repair'
        })
    

    def wait_for_crash(self):

        while self.in_use:
            a = self.sense.get_accelerometer_raw()
            x, y, z = abs(a['x']), abs(a['y']), abs(a['z'])
            if (x - (y + z) >= self.threashold or y - (x + z) >= self.threashold or z - (x + y) >= self.threashold):
                self.ask_for_repair()
    

    def starting_detection(self):
        self.in_use = True
        self.wait_for_crash()
        
            
