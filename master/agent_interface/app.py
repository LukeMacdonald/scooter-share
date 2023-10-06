import re
from functools import wraps
from passlib.hash import sha256_crypt
from agent.common import socket_utils
from master.agent_interface import comms
from master.database.models import RepairStatus, ScooterStatus, BookingState
import master.database.queries as queries
import master.web.database.scooters as scooter_api
import master.web.database.bookings as booking_api
import master.web.database.users as user_api
import master.web.database.transactions as transaction_api
import master.web.database.repairs as repair_api

# todo: Add validation to all functions

app = None

def app_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

@comms.action("register", ["start"])
@app_context
def register(handler, request):
    try:
        role = request.get("role")
        email = request.get("email")
        phone_number = request.get('phone_number')
         
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address format.")
                 
        existing_user = user_api.get_by_email(email)
        if existing_user:
            raise ValueError("Email address already registered.")
        
        phone_regex = r'^[0-9]{10}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("Invalid phone number format.")
        
        user = user_api.post(request)
        handler.state = role
        return {"user": user, "response": "yes"}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": "Internal Server Error."}

@comms.action("login", ["start", "customer", "engineer"])
@app_context
def login(handler, request):
    email = request["email"]
    user = user_api.get_by_email(email)
    if user is None:
        return {"error": "Email not found."} 
    if not sha256_crypt.verify(request["password"], user.password):
        return {"error": "Password is incorrect."}
    
    handler.state = user.role
    return {"user": user.as_json()}

@comms.action("locations", ["engineer"])
@app_context
def fetch_reported_scooters(handler, request):
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    return {"data": queries.scooters_awaiting_repairs()}

@comms.action("repair-fixed", ["engineer"])
@app_context
def update_status(handler, request):
    """
    Mark scooter as repaired by updating its status as available.

    Args:
        scooter_id (int): The ID of the scooter to update.
        repair_id (int): The ID of the repair associated with the scooter.

    Returns:
        dict: A dictionary containing the response data or an error message.
    """
    message, status = queries.fix_scooter(request["scooter_id"], request["repair_id"])
    if status == 200:
        return {"message": message}
    else:
        return {"error": status}
    
@comms.action("customer-homepage", ["customer"])
@app_context
def fetch_available_scooters(handler, request):
    """
    Fetch a list of available scooters.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        customer_id = int(request.get("customer_id"))
        if customer_id is None:
            raise ValueError("CustomerID not found passed!") 
        
        scooters = scooter_api.get_by_status(ScooterStatus.AVAILABLE.value)
        bookings = booking_api.get_by_user(customer_id)
        customer = user_api.get(customer_id)
        
        if customer is None:
            raise ValueError("Customer not found.")
        
        data = {
            "scooters": scooters,
            "bookings": bookings,
            "user_details": customer
        }
        return data
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": "Internal Server Error."}
    
@comms.action("make-booking", ["customer"])
@app_context
def make_booking(handler, request):
    """
    Handles the booking creation and updates scooter status to 'OCCUPYING'.

    Args:
        handler: The handler object.
        request (dict): The booking request data.

    Returns:
        dict: A dictionary containing the response message.
    """
    try:
        booking_data = request.get("data")
        if booking_data is None:
            raise ValueError("Booking data not passed!")
        booking = booking_api.post(booking_data)
        scooter_id = booking.get("scooter_id")
        
        if scooter_id:
            scooter_api.update_status(scooter_id, ScooterStatus.OCCUPYING.value)
            return {"message": "Booking created successfully."}
        else:
            raise ValueError("Invalid scooter ID in the booking data.")
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": "Internal Server Error."}

@comms.action("cancel-booking", ["customer"])
@app_context
def cancel_booking(handler, request):
    """
    Updates a booking to have the status 'cancelled' in the database.

    Returns:
        dict: A dictionary containing the response message.
    """
    try:
        booking_id = request.get("booking-id")
        booking = booking_api.update_status(booking_id, BookingState.CANCELLED.value)
        if booking:
            scooter_id = booking["scooter_id"]
            scooter_api.update_status(scooter_id, ScooterStatus.AVAILABLE.value)
            return {"message": "Booking successfully cancelled."}
        else:
            return {"error": "Booking not found."}
    except Exception as e:
        return {"error": str(e)}
    
@comms.action("report-issue", ["customer"])
@app_context
def submit_repair_request(handler, request):
    """
    Updates a scooter to have the status 'awaiting-repair' in the database.

    Returns:
        dict: A dictionary containing the response message.
    """
    try:
        scooter_id = request.get("scooter-id")
        if scooter_id is None:
            raise ValueError("ScooteID not passed!") 
        report_text = request.get("report")
        if report_text is None:
            raise ValueError("Report Details Not Passed!") 
        
        repair_api.post(scooter_id, report_text, RepairStatus.PENDING.value)
        scooter_api.update_status(scooter_id, ScooterStatus.AWAITING_REPAIR.value)
        
        return {"message": "Repair request submitted successfully."}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error."}
    
@comms.action("top-up-balance", ["customer"])
@app_context
def top_up_balance(handler, request):
    """
    Updates the balance of a user.

    Returns:
        dict: An empty dictionary if no errors occured.
    """
    try:
        amount = float(request.get("amount", 0))
        user_id = request.get("user-id")
        user = user_api.get(int(user_id))
        if user is None: 
            raise ValueError("User not found")
        user["balance"] += amount
        updated_user = user_api.update(user_id, user)
        if updated_user is None:
            raise ValueError("Update user failed!") 
        transaction_api.post(user_id, amount=amount)
        return {"new_balance": user["balance"]}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": "Internal Server Error"}
    

@comms.action("get-scooter-by-id", ['start'])
def fetch_scooters_by_id(handler, request):
    """
    Fetch a list of scooters.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    with app.app_context():
        scooters = scooter_api.get(request['scooter_id'])
        data = {
            "scooters" : scooters,
        }
        return data
# def lock_scooter(handler, request):-
def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
