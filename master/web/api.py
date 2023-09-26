from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

app = Flask(__name__)

@app.route("/")
def root():
    return "Good morning everyone!"

@app.route("/register")
def register():

    try:
        data = {
            #Auto assign an id?
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name')
        }
        response = requests.post(path='http://localhost:5000/user', json=data)

    except Exception as e:
        print(e)

@app.route("/login")
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        response = requests.get(path='http://localhost:5000/user/{}'.format(username))

        # check that corresponding username and password are correct
        response("username")
        if(sha256_crypt.verify(password, hashedPassword))

        # direct to page corresponding to user type if successful

    except Exception as e:
        print(e)