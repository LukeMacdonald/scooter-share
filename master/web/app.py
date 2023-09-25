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
        response = requests.post(path='/user', json=data)

    except Exception as e:
        print(e)

@app.route("/login_user")
def login_user():
    id = request.form.get('id')
    password = request.form.get('password')
    login_type = request.form.get('login_type')
    try:
        response = requests.get('/user/{}'.format(id))

        # direct to page corresponding to login type if successful

    except Exception as e:
        print(e)