from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib import sha256_crypt
import os, requests, json

app = Flask(__name__)

def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # communicate with the master

    # if receives confirmation and user type from master

    # if user type is user
    redirect(url_for('user_homepage'))

    # if user type is admnin
    redirect(url_for('admin_homepage'))

    # if user type is engineer
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
    
