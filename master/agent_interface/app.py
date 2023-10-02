from agent.common import socket_utils
from agent.common import socket_utils
from constants import API_BASE_URL
from flask import jsonify
import json
from master.agent_interface import comms
from master.agent_interface import comms
from master.database.database_manager import db
from master.database.database_manager import db
from master.database.models import Booking, RepairStatus, Repairs, Scooter, ScooterStatus, User, UserType
from master.database.models import User, UserType, Scooter, Booking, ScooterStatus
import master.database.queries as queries
from passlib.hash import sha256_crypt

app = None

@comms.action("register", ["start"])
def register(handler, request):
    if request["role"] not in [UserType.CUSTOMER.value, UserType.ENGINEER.value]:
        raise ValueError("role must be either customer or engineer")
    password_hash = sha256_crypt.hash(request["password"])
    user = User(username=request["password"],
                password=password_hash,
                email=request["email"],
                first_name=request["first_name"],
                last_name=request["last_name"],
                role=request["role"])
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    handler.state = request["role"]
    return {"user": user.as_json(), "response": "yes"}

@comms.action("login", ["start"])
def login(handler, request):
    email = request["email"]
    with app.app_context():
        user = User.query.filter_by(email=email).first()
    if user is None or not sha256_crypt.verify(request["password"], user.password):
        return {"error": "Login info is incorrect."}
    else:
        handler.state = user.role
        return {"user": user.as_json()}

@comms.action("locations", ["engineer"])
def fetch_reported_scooters(handler, request):
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    with app.app_context():
        return {"data": queries.scooters_awaiting_repairs()}

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
        message, status = queries.fix_scooter(request["scooter_id"], request["repair_id"])
        if status == 200:
            return {"message": message}
        else:
            return {"error": status}
    
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
    
@comms.action("make-booking", ["start"])
def make_booking(handler, request):
    booking_data = request["data"]
    booking = Booking(user_id=booking_data["user_id"],
                      scooter_id=booking_data["scooter_id"],
                      date=booking_data["date"],
                      start_time=booking_data["start_time"],
                      end_time=booking_data["end_time"],
                      status=booking_data["status"])
    with app.app_context():
        scooter = Scooter.query.get(booking_data["scooter_id"])
        scooter.status = ScooterStatus.OCCUPYING.value
        db.session.add(booking)
        db.session.commit()
    return {}

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
