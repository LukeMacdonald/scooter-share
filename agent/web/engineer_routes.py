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

def communicate_with_server(message_to_server):
    """
    Communicate with the server over a socket connection.

    Args:
        message_to_server (dict): The message to send to the server.

    Returns:
        dict or None: The server's response as a dictionary, or None on error.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            sendJson(s, message_to_server)
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

def fetch_scooter_locations():
    """
    Send a request to the server to fetch scooter locations.

    Returns:
        dict or None: The fetched scooter locations as a dictionary, or None on error.
    """
    message_to_server = {"name": "locations"}
    return communicate_with_server(message_to_server)

def update_scooter_status(id):
    """
    Update the status of a scooter on the server.

    Args:
        id (str): The ID of the scooter to update.

    Returns:
        dict or None: The server's response as a dictionary, or None on error.
    """
    message_to_server = {"name": "repair-fixed", "id": id}
    return communicate_with_server(message_to_server) 

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
    
    return render_template("engineer/pages/locations.html", scooter_data=scooter_data)

@engineer.route("/engineer/scooters/repairs")
def update_repair_report():
    """
    Display the update repair report page for engineers.

    Returns:
        Flask response: The update repair report page.
    """
    scooter_data = fetch_scooter_locations()
    return render_template("engineer/pages/update_repair.html", scooter_data=scooter_data)

@engineer.route("/engineer/scooter/fixed", methods=["POST"])
def scooter_fixed():
    """
    Handle the scooter fixed form submission for engineers.

    Returns:
        Flask redirect: Redirects back to the update repair report page.
    """
    scooter_id = request.form.get("scooter_id")
    update_scooter_status(scooter_id)
    return redirect(url_for("engineer.update_repair_report"))