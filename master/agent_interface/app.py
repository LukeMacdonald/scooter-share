import re
import requests
from functools import wraps
from passlib.hash import sha256_crypt
from agent.common import socket_utils
from master.agent_interface import comms
from master.database.models import RepairStatus, ScooterStatus, BookingState
import master.database.queries as queries

API_BASE_URL = "http://localhost:5000"

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
        response = requests.get(f"{API_BASE_URL}/user/email/{email}", timeout=5)
        
        if response.status_code == 200: 
            raise ValueError("Email address already registered.")
        
        phone_regex = r'^[0-9]{10}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("Invalid phone number format.")
        
        user = requests.post(f"{API_BASE_URL}/user", json=request, timeout=5).json()
        handler.state = role
        return {"user": user, "response": "yes"}
    except ValueError as error:
        return {"error": str(error)}

@comms.action("login", ["start", "customer", "engineer"])
@app_context
def login(handler, request):
    email = request["email"]
    response = requests.get(f"{API_BASE_URL}/user/email/{email}", timeout=5)
    if response.status_code == 404:
        return {"error": "Email not found."}
    user = response.json()
    if not sha256_crypt.verify(request["password"], user["password"]):
        return {"error": "Password is incorrect."}
    handler.state = user["role"]
    return {"user": user}

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
        
        scooters = requests.get(f"{API_BASE_URL}/scooters/status/{ScooterStatus.AVAILABLE.value}", timeout=5).json() 
        bookings = requests.get(f"{API_BASE_URL}/bookings/user/{customer_id}", timeout=5).json()
        response = requests.get(f"{API_BASE_URL}/user/id/{customer_id}", timeout=5)
            
        if response.status_code == 404: 
            raise ValueError("Customer not found.")
        
        data = {
            "scooters": scooters,
            "bookings": bookings,
            "user_details": response.json()
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
        
        booking = requests.post(f"{API_BASE_URL}/bookings", json=booking_data, timeout=5).json()
        scooter_id = booking.get("scooter_id")
        
        if scooter_id:
            data = {"status":ScooterStatus.OCCUPYING.value}
            updated_repair = requests.put(f"{API_BASE_URL}/scooter/status/{scooter_id}", json=data, timeout=5).json()  
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
        data = {"status": BookingState.CANCELLED.value }
        response = requests.put(f"{API_BASE_URL}/booking/status/{booking_id}", json=data, timeout=5)
        if response.status_code != 404:
            booking = response.json()
            scooter_id = booking["scooter_id"]
            data = {"status":ScooterStatus.AVAILABLE.value}
            updated_repair = requests.put(f"{API_BASE_URL}/scooter/status/{scooter_id}", json=data, timeout=5).json()
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
        
        data = {
            "scooter_id": scooter_id,
            "report": report_text,
            "status": RepairStatus.PENDING.value
        }
        
        repair = requests.post(f"{API_BASE_URL}/repair", json=data, timeout=5).json()
        data = {"status":ScooterStatus.AWAITING_REPAIR.value}
        updated_repair = requests.put(f"{API_BASE_URL}/scooter/status/{scooter_id}", json=data, timeout=5).json()
        
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
        response = requests.get(f"{API_BASE_URL}/user/id/{user_id}", timeout=5)
        if response.status_code == 404: 
            raise ValueError("User not found")
        user = response.json()
        user["balance"] += amount
        response = requests.put(f"{API_BASE_URL}/user/{user_id}",json=user, timeout=5)
        if response.status_code == 404: 
            raise ValueError("Update user failed!") 
        
        data = {"user_id": user_id, "amount":amount}
        requests.post(f"{API_BASE_URL}/transaction",json=data, timeout=5).json() 
        return {"new_balance": user["balance"]}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": "Internal Server Error"}

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
