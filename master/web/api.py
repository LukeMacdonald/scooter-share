from flask import Flask
from passlib import sha256_crypt
import requests

app = Flask(__name__)

@app.route("/")
def root():
    return "Good morning everyone!"

@app.route("/register")
def register(data):

    try:
        response = requests.post(path='http://localhost:5000/user', json=data)

    except Exception as e:
        print(e)

@app.route("/login")
def login_user(username, password):

    try:
        response = requests.get(path='http://localhost:5000/user/{}'.format(username))

        # if username exists and 
        if(sha256_crypt.verify(password, hashedPassword)):
            # send confirmation and user type to the agent

    except Exception as e:
        print(e)