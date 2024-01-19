from flask import Flask
from gps3 import gps3
from geopy.geocoders import Nominatim

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

app = Flask(__name__)


@app.route("/")
def hello_world():
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print(str(data_stream.TPV['time']) + " | " + str(data_stream.TPV['lat']) + " | " + str(data_stream.TPV['lon']) + " | " + str(data_stream.TPV['alt']))
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)    

    