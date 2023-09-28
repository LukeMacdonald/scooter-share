"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
import socket
import logging
from flask import Blueprint, render_template, url_for, redirect, request
from agent_common.socket_utils import sendJson, recvJson

engineer = Blueprint("engineer", __name__)

HOST = "192.168.1.98"
ENGINEER_SOCKET_PORT = 63000
ADDRESS = (HOST, ENGINEER_SOCKET_PORT)

logging.basicConfig(level=logging.ERROR)

def communicate_with_master(master_request):
    """
    Communicate with the master pi over a socket connection.

    Args:
        message_to_master (dict): The message to send to the master.

    Returns:
        dict or None: The master pi's response as a dictionary, or None on error.
    """
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            sendJson(s, master_request)
            while True:
                data = recvJson(s)
                if "error" in data:
                    raise Exception(data['error'])
                elif "data" in data:
                    return data["data"]
    except ConnectionRefusedError:
        logging.error("Connection to the server was refused.")
    except TimeoutError:
        logging.error("Socket operation timed out.")
    except Exception as error:
        logging.error(str(error))
    return None

@engineer.route("/engineer")
def home():
    """
    Display the engineer home page.

    Returns:
        Flask response: The engineer home page.
    """
    master_request = {"name": "locations"}
    response = communicate_with_master(master_request)
    return render_template("engineer/pages/home.html", scooter_data=response)

@engineer.route("/engineer/scooters/locations")
def scooter_locations(): 
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """
    master_request = {"name": "locations"}
    response = communicate_with_master(master_request)
    return render_template("engineer/pages/locations.html", scooter_data=response)

@engineer.route("/engineer/scooters/repairs")
def update_repair_report():
    """
    Display the update repair report page for engineers.

    Returns:
        Flask response: The update repair report page.
    """
    master_request = {"name": "locations"}
    response = communicate_with_master(master_request)
    return render_template("engineer/pages/update_repair.html", scooter_data=response)

@engineer.route("/engineer/scooter/fixed", methods=["POST"])
def scooter_fixed():
    """
    Handle the scooter fixed form submission for engineers.

    Returns:
        Flask redirect: Redirects back to the update repair report page.
    """
    scooter_id = request.form.get("scooter_id")
    master_request = {"name": "repair-fixed", "id": scooter_id}
    communicate_with_master(master_request)
    return redirect(url_for("engineer.update_repair_report"))