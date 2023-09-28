"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
import socket
from flask import Blueprint, render_template, url_for, redirect, request
from agent_common.socket_utils import sendJson, recvJson

engineer = Blueprint("engineer", __name__)

HOST = "192.168.1.98"
ENGINEER_SOCKET_PORT = 63000
ADDRESS = (HOST, ENGINEER_SOCKET_PORT)

def fetch_scooter_locations():
    """
    Send a request to the server to fetch scooter locations.

    Returns:
        dict or None: The fetched scooter locations as a dictionary, or None on error.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            message_to_server = {"name": "locations"}    
            sendJson(s, message_to_server)
            while True:
                data = recvJson(s)
                if "Message" in data:
                    return data["Message"]
    except Exception as error:
        print(f"An unexpected error occurred: {str(error)}")
    return None

def update_scooter_status(id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            message_to_server = {"name": "repair-fixed","id": id}
            sendJson(s, message_to_server)
            while True:
                data = recvJson(s)
                if "Message" in data:
                    return data["Message"]
    except Exception as error:
        print(f"An unexpected error occurred: {str(error)}")  

@engineer.route("/engineer")
def home():
    """
    Display the engineer home page.

    Returns:
        Flask response: The engineer home page.
    """
    scooter_data = fetch_scooter_locations()
    return render_template("engineer/pages/home.html", scooter_data=scooter_data)

@engineer.route("/engineer/scooters/locations")
def scooter_locations(): 
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """
    scooter_data = fetch_scooter_locations()

    # if scooter_data is not None:
    #     print(scooter_data)
    #     print()
    
    return render_template("engineer/pages/locations.html", scooter_data=scooter_data)

@engineer.route("/engineer/scooters/repairs")
def update_repair_report():
    scooter_data = fetch_scooter_locations()
    return render_template("engineer/pages/update_repair.html", scooter_data=scooter_data)

@engineer.route("/engineer/scooter/fixed", methods=["POST"])
def scooter_fixed():
    scooter_id = request.form.get("scooter_id")
    update_scooter_status(scooter_id)
    print(scooter_id)
    return redirect(url_for("engineer.update_repair_report"))