from flask import Flask
from geopy.geocoders import Nominatim

app = Flask(__name__)

app.run(host='0.0.0.0', port=5000, debug=True)    

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/location')
def location():
    #todo: Function to get location of scooter
    pass

@app.route('/lock', methods=['POST'])
def lock():
    #todo: Function which will lock the scooter
    pass

@app.route('/unlock')
def unlock():
    #todo: Function which will unlock the scooter
    pass

@app.route('/auth')
def authenticate():
    #todo: Function to authenticate user using face recognition
    pass