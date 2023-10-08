import threading
from sense_hat import SenseHat
from time import sleep

from agent.scooter.status import Status
from agent.scooter.facial_recognition.facial_recognition import FacialRecognition
from agent.scooter.crash_detection import CrashDetection
from agent.web.connection import get_connection


class ScooterInterface():
    def __init__(self, scooter_id:int) -> None:
        self.crash_detection = CrashDetection(scooter_id)
        self.sense = SenseHat()
        self.scooter_id = scooter_id


    def check_booking(self, user_id):
        message = get_connection().send({
            'scooter_id': self.scooter_id,
            'user_id': user_id,
            'name': 'check-booking'
        })
        if message['message'] == 'Unlocking Scooter':
            self.activate_scooter(user_id)
        else:
            print(message['message'])
            self.run_facial_recognition()


    def activate_scooter(self, user_id):
        message = get_connection().send({
            'scooter_id': self.scooter_id,
            'user_id': user_id,
            'name': 'unlock-scooter'
        })
        print(message['message'])
        if message['message'] == 'Scooter Unlocked':
            being_used = True
            self.crash_detection_thread = threading.Thread(target=self.crash_detection.starting_detection)
            self.crash_detection_thread.start()
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
        self.crash_detection.in_use = False
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
                    if event.direction == 'middle':
                        scanning = True
                        face_recog = FacialRecognition(self.scooter_id)
                        user_id = face_recog.recognize()
                        if user_id == -1:
                            print('An internal server error has occured')
                            self.run_facial_recognition()
                            exit()
                        break
                    elif event.direction == 'down':
                        scanning = True
                        valid_user = False
                        while not valid_user:
                            print('Please Enter your email: ', end='')
                            email = input()
                            if email == 'return':
                                self.run_facial_recognition()
                                exit()
                            response = get_connection().send({
                                'email': email,
                                'name': 'get-user-by-email'
                            })
                            if response['message'] == 'invalid email':
                                print(response['message'])
                                continue
                            else:
                                valid_user = True
                                user_id = response['user_id']
                        break
        self.check_booking(user_id)
        

    def scooter_startup(self):
        status_thread = threading.Thread(target=self.run_status_display)
        status_thread.start()
        recognition_thread = threading.Thread(target=self.run_facial_recognition)
        recognition_thread.start()