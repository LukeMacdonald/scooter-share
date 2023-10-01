from agent.common import socket_utils
from flask import jsonify
from master.agent_interface import comms
from master.database.database_manager import db
from master.database.models import Booking, RepairStatus, Repairs, Scooter, ScooterStatus, User, UserType
from master.database.queries import scooters_awaiting_repairs
from passlib.hash import sha256_crypt
from requests.exceptions import RequestException
import requests

app = None

@comms.action("register", ["start"])
def register(handler, message):
    if message["role"] not in [UserType.CUSTOMER.value, UserType.ENGINEER.value]:
        raise ValueError("role must be either customer or engineer")
    password_hash = sha256_crypt.hash(message["password"])
    user = User(username=message["password"],
                password=password_hash,
                email=message["email"],
                first_name=message["first_name"],
                last_name=message["last_name"],
                role=message["role"])
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    handler.state = message["role"]
    return {"user": user.as_json(), "response": "yes"}

@comms.action("login", ["start"])
def login(handler, message):
    password_hash = sha256_crypt.hash(message["password"])
    # need to decrypt password and compare
    email = message["email"]
    with app.app_context():
        user = User.query.filter_by(email=email).first()
    handler.state = user.role
    return {"user": user.as_json(), "response": "yes"}

@comms.action("locations", ["engineer"])
def fetch_reported_scooters(handler, request):
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    with app.app_context():
        return {"data": scooters_awaiting_repairs()}

@comms.action("repair-fixed", ["engineer"])
def update_scooter_status(handler, request):
    """
    Mark scooter as repaired by updating its status as available.

    Args:
        scooter_id (int): The ID of the scooter to update.
        repair_id (int): The ID of the repair associated with the scooter.

    Returns:
        dict: A dictionary containing the response data or an error message.
    """
    with app.app_context():
        repair_id = request["repair_id"]
        scooter_id = request["scooter_id"]
        scooter = Scooter.query.get(scooter_id)
        repair = Repairs.query.get(repair_id)
        if scooter is None:
            return {"error": f"Scooter with ID {scooter_id} not found"}
        if repair is None:
            return {"error": f"Repair with ID {repair_id} not found"}
        scooter.status = ScooterStatus.AVAILABLE.value
        repair.status = RepairStatus.COMPLETED.value
        db.session.commit()
    return {"message": "Scooter successfully repaired"}
    
@comms.action("customer-homepage", ["customer"])
def fetch_available_scooters(handler, request):
    """
    Fetch a list of available scooters.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    with app.app_context():
        scooters = Scooter.query.filter_by(status="available")
        bookings = Booking.query.filter_by(user_id=request["customer_id"])
        data = {
            "scooters" : [s.as_json() for s in scooters],
            "bookings" : [b.as_json() for b in bookings]
        }
        return data

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
