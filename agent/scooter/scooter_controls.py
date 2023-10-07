import threading
from sense_hat import SenseHat
from time import sleep

from agent.scooter.status import Status
from agent.scooter.facial_recognition.facial_recognition import FacialRecognition
from agent.web.connection import get_connection


class ScooterInterface():
    def __init__(self, scooter_id:int) -> None:
        self.sense = SenseHat()
        self.scooter_id = scooter_id


    def activate_scooter(self, user_id):
        message = get_connection().send({
            'scooter_id': self.scooter_id,
            'user_id': user_id,
            'name': 'unlock-scooter'
        })
        print(message['message'])
        being_used = True
        while being_used:
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    being_used = False
                    break
        self.deactivate_scooter()



    def deactivate_scooter(self):
        get_connection().send({
            'scooter_id': self.scooter_id,
            'name': 'lock-scooter'
        })
        self.run_facial_recognition()
        

    def run_status_display(self):
        status = Status(self.scooter_id)
        while True:
            sleep(2.0)
            status.update_local_status()

    def run_facial_recognition(self):
        print('Ready')
        scanning = False
        while not scanning:
            for event in self.sense.stick.get_events():
                if event.action == 'pressed':
                    scanning = True
                    break
        face_recog = FacialRecognition(self.scooter_id)
        user_id = face_recog.recognize()
        if user_id == -1:
            print('An internal server error has occured')
            self.run_facial_recognition()
            exit()
        self.activate_scooter(user_id)
        

    def scooter_startup(self):
        status_thread = threading.Thread(target=self.run_status_display)
        status_thread.start()
        recognition_thread = threading.Thread(target=self.run_facial_recognition)
        recognition_thread.start()