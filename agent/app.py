from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib import sha256_crypt
import os, requests, json
from agent_common import comms

app = Flask(__name__)
connection = comms.Connection()

def login():
    username = request.form.get('username')
    password = request.form.get('password')

    data = {
        "username": username,
        "password": password,
        "name": "login"
    }
    
    # communicate with the master
    response = connection.send(data)
    # if receives confirmation and user type from master
    if response["name"] == "yes":
        if response["user_type"] == "user":
            redirect(url_for('user_homepage'))
        elif response["admin_type"] == "admin":
            redirect(url_for('admin_homepage'))
        elif response["engineer_type"] == "engineer":
            redirect(url_for('engineer_homepage'))

def signup():
    data = {
            #Auto assign an id?
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name')
        }
    
    #send this data to the master
    
