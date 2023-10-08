from agent.scooter.facial_recognition.facial_recognition import FacialRecognition
from agent.web.connection import get_connection

print('add face for user id: ', end='')
user_id = input()

fr = FacialRecognition(scooter_id=1)
fr.get_photo(user_id=user_id)




