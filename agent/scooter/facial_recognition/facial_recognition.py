

import cv2
import os
import face_recognition
import imutils
from datetime import datetime
from imutils.video import VideoStream




class facial_recognition():
    def __init__(self, user:str) -> None:
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)
        self.camera.set(4, 480)
        self.user = user

    
    def __delattr__(self, __name: str) -> None:
        self.camera.release()

    def get_photo(self):

        ret, frame = self.camera.read()
        if not ret:
            print(f'No camera detected.')
            return 1


        face_cascade = cv2.CascadeClassifier('agent/scooter/facial_recognition/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(face) == 0:
            print(f'No face detected, restarting')
            self.get_photo()
            exit()
        
        print('got face')
        
        for x, y, w, h in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            image_name = f'{self.user}_{datetime.now()}.jpg'


        self.image = frame
        self.encode_photo()

    def encode_photo(self):
        print('encoding')

        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(self.image)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            self.add_encoding(encoding)


    def recognize(self):
        stream = VideoStream(src=0).start()
        data = self.get_encodings()

        while True:

            frame = stream.read()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=240)

            boxes = face_recognition.face_location(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)
            users = []

            for encoding in encodings:
                matches = face_recognition.compare_faces(data['encodings'], encoding)
                user = ''

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        user = data['user'][i]
                        counts[user] = counts.get(user, 0) + 1
                    stream.stop()
                    return max(counts, key=counts.get)


    def add_encoding(self, e):
        '''
            add user and encoding data to database
        '''
        print(e)

    def get_encodings(self):
        '''
            get user and encoding data from database
        '''
        

if __name__ == '__main__':
    recognizer = facial_recognition('name')
    recognizer.get_photo()
    del recognizer.camera
    recognizer.encode_photo()