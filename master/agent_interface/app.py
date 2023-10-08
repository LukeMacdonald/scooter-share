import re
import requests
from functools import wraps
from passlib.hash import sha256_crypt
from agent.common import socket_utils
from master.agent_interface import comms
from master.database.models import RepairStatus, ScooterStatus, BookingState
import master.database.queries as queries

API_BASE_URL = "http://localhost:5000"

# Functions which check the status, because most of the time we just
# want to fail fast if they fail somehow. Pass check_status=False if you
# will handle errors.
def get_request(endpoint, check_status=True):
    request = requests.get(API_BASE_URL + endpoint)
    if check_status:
        request.raise_for_status()
    return request
def post_request(endpoint, check_status=True, **kwargs):
    request = requests.post(API_BASE_URL + endpoint, **kwargs)
    if check_status:
        request.raise_for_status()
    return request
def put_request(endpoint, check_status=True, **kwargs):
    request = requests.put(API_BASE_URL + endpoint, **kwargs)
    if check_status:
        request.raise_for_status()
    return request

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

        response = get_request(f"/user/email/{email}", check_status=False)
        if response.status_code == 200: 
            raise ValueError("Email address already registered.")
        
        phone_regex = r'^[0-9]{10}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("Invalid phone number format.")
        
        user = post_request("/user", json=request).json()
        handler.state = role
        return {"user": user, "response": "yes"}
    except ValueError as error:
        return {"error": str(error)}

@comms.action("login", ["start", "customer", "engineer"])
@app_context
def login(handler, request):
    email = request["email"]
    response = get_request(f"/user/email/{email}", check_status=False)
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
        if "customer_id" not in request:
            raise ValueError("customer_id was not supplied.")
        customer_id = int(request.get("customer_id"))

        scooters = get_request(f"/scooters/status/{ScooterStatus.AVAILABLE.value}").json()
        bookings = get_request(f"/bookings/user/{customer_id}").json()
        response = get_request(f"/user/id/{customer_id}", check_status=False)
            
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
        return {"error": str(error)}
    
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
        
        booking = post_request("/bookings", json=booking_data).json()
        scooter_id = booking.get("scooter_id")

        if scooter_id:
            data = {"status":ScooterStatus.OCCUPYING.value}
            response = put_request(f"/scooter/status/{scooter_id}", json=data)
            if response.status_code == 400 or response.status_code == 404:
                return {"error": response.json['message']}
            return {"message":"Booking successfuly made"}
        else:
            raise ValueError("Invalid scooter ID in the booking data.")
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": str(error)}

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
        data = {"status": BookingState.CANCELLED.value}
        response = put_request(f"/booking/status/{booking_id}", json=data)
        if response.status_code != 404:
            booking = response.json()
            scooter_id = booking["scooter_id"]
            
            data = {"status":ScooterStatus.AVAILABLE.value}
            response = put_request(f"/scooter/status/{scooter_id}", json=data)
            
            if response.status_code in [400, 404]:
                return {"error": response.json['message']}
            return {"message":"Booking successfuly cancelled"}
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
        
        response = post_request("/repair", json=data)
        
        if response.status_code in [400, 404]:
           return {"error": response.json['message']}
       
        data = {"status":ScooterStatus.AWAITING_REPAIR.value}
        response = put_request(f"/scooter/status/{scooter_id}", json=data)
        if response.status_code in [400, 404]:
           return {"error": response.json['message']} 
        
        return {"message": "Repair request submitted successfully."}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}
    
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
        response = get_request(f"/user/id/{user_id}")
        if response.status_code == 404: 
            raise ValueError("User not found")
        user = response.json()
        user["balance"] += amount

        response = put_request(f"/user/{user_id}", json=user, check_status=False)
        if response.status_code == 404:
            raise ValueError("Update user failed!") 
        
        data = {"user_id": user_id, "amount":amount}
        post_request("/transaction", json=data)
        return {"new_balance": user["balance"]}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error: 
        return {"error": str(error)}
    

@comms.action("get-scooter-by-id", ['start'])
def fetch_scooters_by_id(handler, request):
    """
    Fetch a list of scooters.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        scooter_id = int(request.get("scooter_id"))
        if scooter_id is None:
            raise ValueError("ScooterID not found passed!")
        
        scooters = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5).json() 
        data = scooters
        
        return data

    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@comms.action("get-faces", ['start'])
def get_faces(handler, request):
    """
        add a face to the registry

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        
        response = requests.get(f"{API_BASE_URL}/face/all", timeout=5).json()
        return response

    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@comms.action('unlock-scooter', ['start'])
def unlock_scooter(handler, request):

    data = {
        'scooter_id': request.get('scooter_id'),
        'user_id': request.get('user_id')
    }

    user_info = requests.get(f"{API_BASE_URL}/user/id/{data['user_id']}", timeout=5).json()
    scooter_info = requests.get(f"{API_BASE_URL}/scooter/id/{data['scooter_id']}", timeout=5).json()

    if scooter_info['status'] != ScooterStatus.AVAILABLE.value:
        return {"message": "Scooter Not Available"}

    if user_info['balance'] < scooter_info['cost_per_time']:
        return {"message": "insufficient funds"}
    else:
        user_info['balance'] -= scooter_info['cost_per_time']
        scooter_update = {"status": ScooterStatus.OCCUPYING.value}
        print(user_info)
        requests.put(f"{API_BASE_URL}/user/{data['user_id']}", json=user_info, timeout=5).json()
        requests.put(f"{API_BASE_URL}/scooter/status/{data['scooter_id']}", json=scooter_update, timeout=5).json()
        return {"message": "Scooter Successfully Booked"}


@comms.action("create-face", ['start'])
def create_face(handler, request):
    """
        add a face to the registry

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:

        data = {
            'user_id': request.get('user_id'),
            'face': request.get('face')
        }
        
        requests.post(f"{API_BASE_URL}/face", json=data, timeout=5).json() 

    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": 'internal server error'}


@comms.action("get-faces", ['start'])
def get_faces(handler, request):
    """
    Get all the faces in the registry.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/face/all", timeout=5).json()
        return response
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@comms.action('unlock-scooter', ['customer'])
def unlock_scooter(handler, request):

    data = {
        'scooter_id': request.get('scooter_id')
    }

    scooter_info = requests.get(f"{API_BASE_URL}/scooter/id/{data['scooter_id']}", timeout=5).json()
    scooter_update = {'status': ScooterStatus.UNLOCKED.value}
    requests.put(f"{API_BASE_URL}/scooter/status/{data['scooter_id']}", json=scooter_update, timeout=5).json()
    return {"message": "Scooter Successfully Unlocked"}


@comms.action('lock-scooter', ['customer'])
def lock_scooter(handler, request):

    data = {
        'scooter_id': request.get('scooter_id'),
        'user_id': request.get('user_id')
    }
    response = requests.get(f"{API_BASE_URL}/booking/user/{data['user_id']}").json()

    booking_update = {'status': BookingState.COMPLETED.value}
    scooter_update = {'status': ScooterStatus.AVAILABLE.value}

    requests.put(f"{API_BASE_URL}/booking/status/{response['booking_id']}", json=booking_update, timeout=5).json()
    requests.put(f"{API_BASE_URL}/scooter/status/{data['scooter_id']}", json=scooter_update, timeout=5).json()
    return {"message": "Scooter Successfully Returned"}


@comms.action('request-repair', ['start'])
def request_repair(handler, request):

    data = {
        'scooter_id': request.get('scooter_id')
    }

    scooter_update = {'status': ScooterStatus.AWAITING_REPAIR.value}
    requests.put(f"{API_BASE_URL}/scooter/status/{data['scooter_id']}", json=scooter_update, timeout=5).json()
    return {"message": "Scooter Waiting for Repair"}

@comms.action('check-booking', ['start'])
def check_booking(handler, request):
    data = {
        'scooter_id': request.get('scooter_id'),
        'user_id': request.get('user_id')
    }

    response = requests.get(f"{API_BASE_URL}/booking/user/{data['user_id']}")
    if response.status_code == 404:
        return {'message': 'You don\'t have any bookings'}
    if response['user_id'] != data['user_id']:
        return {'message': 'This scooter isn\'t booked by you'}
    else:
        return {'message': 'Unlocking Scooter'}

@comms.action('get-user-by-email', ['start'])
def get_user(handler, request):
    data = {
        'email': request.get('email')
    }

    response = requests.get(f"{API_BASE_URL}/user/email/{data['email']}")
    if response.status_code == 404:
        return {'message': 'invalid email', 'user_id': 0}
    else:
        response = response.json()
        print(response)
        return {'message': 'user found', 'user_id': response['id']}


def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
