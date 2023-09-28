"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
from flask import Blueprint, render_template
from agent_common.comms import Connection
from agent_common.socket_utils import sendJson, recvJson
import socket, json


engineer = Blueprint("engineer", __name__)

HOST = "192.168.1.98"
PORT = 63000
ADDRESS = (HOST, PORT)

@engineer.route("/engineer/scooters/locations")
def scooter_locations(): 
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        message_to_server = {"name": "locations"}    
        sendJson(s, message_to_server)
        while(True):
            data = recvJson(s)
            if("Message" in data):
                message = data["Message"]
                print("Data Transferred.")
                print(message['name'])
                print()
                break
    return render_template("engineer/pages/locations.html")
