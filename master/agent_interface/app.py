from passlib.hash import sha256_crypt
from agent.common import socket_utils
from master.agent_interface import comms
from master.database.database_manager import db
import master.database.models as models
import master.database.queries as queries
from master.web.database.users import add_user

app = None

@comms.action("register", ["start"])
def register(handler, request):
    if request["role"] not in [models.UserType.CUSTOMER.value, models.UserType.ENGINEER.value]:
        raise ValueError("role must be either customer or engineer")
    with app.app_context():
        user = add_user(request)
    handler.state = request["role"]
    return {"user": user, "response": "yes"}

@comms.action("login", ["start"])
def login(handler, request):
    email = request["email"]
    with app.app_context():
        user = models.User.query.filter_by(email=email).first()
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
        scooters = models.Scooter.query.filter_by(status="available")
        bookings = models.Booking.query.filter_by(user_id=request["customer_id"])
        data = {
            "scooters" : [s.as_json() for s in scooters],
            "bookings" : [b.as_json() for b in bookings]
        }
        return data
    
@comms.action("make-booking", ["customer"])
def make_booking(handler, request):
    booking_data = request["data"]
    with app.app_context():
        booking = models.Booking(user_id=booking_data["user_id"],
                          scooter_id=booking_data["scooter_id"],
                          date=booking_data["date"],
                          start_time=booking_data["start_time"],
                          end_time=booking_data["end_time"],
                          status=booking_data["status"])
        scooter = models.Scooter.query.get(booking_data["scooter_id"])
        scooter.status = models.ScooterStatus.OCCUPYING.value
        db.session.add(booking)
        db.session.commit()
    return {}

@comms.action("cancel-booking", ["customer"])
def cancel_booking(handler, request):
    """
    Updates a booking to have the status 'cancelled' in the database.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    with app.app_context():
        booking = models.Booking.query.filter_by(id=request["booking-id"]).first()
        booking.status = models.BookingState.CANCELLED.value
        scooter = models.Scooter.query.get(booking.scooter_id)
        scooter.status = models.ScooterStatus.AVAILABLE.value
        db.session.commit()
        return {}
    
@comms.action("report-issue", ["customer"])
def submit_repair_request(handler, request):
    """
    Updates a scooter to have the status 'awaiting-repair' in the database.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    repair = models.Repairs(scooter_id=request["scooter-id"],
                     report=request["report"],
                     status=models.RepairStatus.PENDING.value)
    with app.app_context():
        db.session.add(repair)
        db.session.commit()
    
@comms.action("top-up-balance", ["customer"])
def top_up_balance(handler, request):
    """
    Updates the balance of a user.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    amount = float(request["amount"])
    transation = models.Transaction(user_id=request["user-id"], amount=amount)
    with app.app_context():
        user = models.User.query.get(request["user-id"])
        user.balance = user.balance + amount
        db.session.add(transation)
        db.session.commit()
        return {"new_balance": user.balance}

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
