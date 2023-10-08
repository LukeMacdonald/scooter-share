

import cv2
import os
import face_recognition
import imutils
import numpy as np
import json
import pickle
import base64
from datetime import datetime
from imutils.video import VideoStream
from agent.web.connection import get_connection



class FacialRecognition():
    def __init__(self, scooter_id) -> None:
        self.scooter_id = scooter_id
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)
        self.camera.set(4, 480)

    
    def __delattr__(self, __name: str) -> None:
        self.camera.release()

    def get_photo(self, user_id):

        ret, frame = self.camera.read()
        if not ret:
            print(f'No camera detected.')
            return 1


        face_cascade = cv2.CascadeClassifier('agent/scooter/facial_recognition/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(face) == 0:
            print(f'No face detected, restarting')
            self.get_photo(user_id)
            exit()
        
        print('got face')
        
        for x, y, w, h in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


        self.encode_photo(user_id, frame)

    def encode_photo(self, user_id, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(rgb, boxes)

        encodings_str = base64.b64encode(pickle.dumps(encodings)).decode() # This cringe af but it's the only thing that i could get working

        self.add_encoding(user_id, encodings_str)


    def recognize(self):
        self.camera.release()
        stream = VideoStream(src=0).start()
        
        data = self.get_encodings()
        if data == []:
            print('No faces available')
            return -1

        while True:

            frame = stream.read()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)
            users = []

            for encoding in encodings:
                for i in range(len(data)):
                    matches = face_recognition.compare_faces(pickle.loads(base64.b64decode(data[i]['face'])), encoding)
                    if True in matches:
                        user = data[i]['user_id']
                        

                        stream.stop()
                        return user



    def add_encoding(self, user_id, e):
        '''
            add user and encoding data to database
        '''
        get_connection().send({
                'user_id': user_id,
                'face': e,
                'name': 'create-face'
            })
        print('added face to db')

    def get_encodings(self):
        '''
            get user and encoding data from database
        '''
        return get_connection().send({
            'name': 'get-faces'
        })
        
