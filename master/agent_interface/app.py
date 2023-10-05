from passlib.hash import sha256_crypt
from agent.common import socket_utils
from master.agent_interface import comms
from master.database.models import RepairStatus, ScooterStatus, BookingState, UserType
import master.database.queries as queries
import master.web.database.scooters as scooter_api
import master.web.database.bookings as booking_api
import master.web.database.users as user_api
import master.web.database.transactions as transaction_api
import master.web.database.repairs as repair_api

# todo: Add validation to all functions

app = None

@comms.action("register", ["start"])
def register(handler, request):
    if request["role"] not in [UserType.CUSTOMER.value, UserType.ENGINEER.value]:
        raise ValueError("role must be either customer or engineer")
    with app.app_context():
        user = user_api.post(request)
    handler.state = request["role"]
    return {"user": user, "response": "yes"}

@comms.action("login", ["start", "customer", "engineer"])
def login(handler, request):
    email = request["email"]
    with app.app_context():
        user = user_api.get_by_email(email) 
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
def update_status(handler, request):
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
        scooters = scooter_api.get_by_status(ScooterStatus.AVAILABLE.value)
        bookings = booking_api.get_by_user(request["customer_id"])
        customer = user_api.get(int(request["customer_id"]))
        data = {
            "scooters" : scooters,
            "bookings" : bookings,
            "user_details": customer
        }
        return data
    
@comms.action("make-booking", ["customer"])
def make_booking(handler, request):
    booking_data = request["data"]
    with app.app_context():
        booking = booking_api.post(booking_data)
        scooter_api.update_status(booking["scooter_id"], ScooterStatus.OCCUPYING.value)
    return {}

@comms.action("cancel-booking", ["customer"])
def cancel_booking(handler, request):
    """
    Updates a booking to have the status 'cancelled' in the database.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    with app.app_context():
        booking = booking_api.update_status(request["booking-id"], BookingState.CANCELLED.value)
        scooter = scooter_api.update_status(booking["scooter_id"], ScooterStatus.AVAILABLE.value )
        return {}
    
@comms.action("report-issue", ["customer"])
def submit_repair_request(handler, request):
    """
    Updates a scooter to have the status 'awaiting-repair' in the database.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    with app.app_context():
        repair_api.post(request["scooter-id"],request["report"], RepairStatus.PENDING.value)
        scooter_api.update_status(request["scooter-id"], ScooterStatus.AWAITING_REPAIR.value)
    
@comms.action("top-up-balance", ["customer"])
def top_up_balance(handler, request):
    """
    Updates the balance of a user.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    try:
        with app.app_context():
            amount = float(request.get("amount", 0))
            user_id = request.get("user-id")
            user = user_api.get(int(user_id))
            if user is None: 
                raise ValueError("User not found")
            user["balance"] += amount
            updated_user = user_api.update(user_id, user)
            if updated_user is None:
                raise ValueError("Update User Failed!") 
            transaction_api.post(user_id, amount=amount)
            return {"new_balance": user["balance"]}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": "Internal Server Error"}

# def lock_scooter(handler, request):-
def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
