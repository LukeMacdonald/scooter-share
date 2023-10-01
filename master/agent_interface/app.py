import requests
from passlib.hash import sha256_crypt
from requests.exceptions import RequestException
from master.agent_interface import comms
from agent_common import socket_utils
from database.models import User, UserType, Scooter, Booking
from database.database_manager import db
from constants import API_BASE_URL
# from credentials.email import send_email
import json


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
        return {"role": user.role, "response": "yes"}

@comms.action("login", ["start"])
def login(handler, message):
    password_hash = sha256_crypt.hash(message["password"])
    email = message["email"]
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'balance': user.balance
        }
    return {"user": data, "response": "yes"}

@comms.action("locations", ["start"])
def fetch_reported_scooters(handler, request):
    """
    Fetch a list of scooters reported for repair.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        url = f"{API_BASE_URL}/scooters/awaiting-repairs"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}
    except RequestException as req_error:
        return {"status_code": 500, "error": f"{req_error}"}
    except ValueError as json_error:
        return {"status_code": 500, "error": f"JSON decoding error while processing response: {json_error}"}
    except Exception as error:
        return {"status_code": 500, "error": f"An unexpected error occurred: {error}"}

@comms.action("repair-fixed", ["start"])
def update_scooter_status(handler, request):
    """
    Mark scooter as repaired by updating its status as available.

    Args:
        scooter_id (int): The ID of the scooter to update.
        repair_id (int): The ID of the repair associated with the scooter.

    Returns:
        dict: A dictionary containing the response data or an error message.
    """
    try:
        repair_id = request["repair_id"]
        scooter_id = request["scooter_id"]
        fixed_url = f"{API_BASE_URL}/scooters/fixed/{scooter_id}/{repair_id}"
        response = requests.put(fixed_url, timeout=5)

        if response.status_code == 200:
            return {"status_code": response.status_code, "message": "Scooter status updated successfully"}
        else:
            return {"status_code": response.status_code, "error": f"Failed to update scooter status. Status code: {response.status_code}"}

    except RequestException as req_error:
        return {"status_code": 500, "error": f"Request error while updating scooter status: {req_error}"}
    except Exception as error:
        return {"status_code": 500, "error": f"An unexpected error occurred: {error}"}

@comms.action("customer-homepage", ["start"])
def fetch_homepage_data(handler, request):
    """
    Fetch a list of available scooters.

    Returns:
        dict: A dictionary containing the fetched data or an error message.
    """
    try:
        with app.app_context():
            scooters = Scooter.query.filter_by(status="available")
            scooters_list = []
            for scooter in scooters:
                scooter_dict = {
                    "id": scooter.id,
                    "make": scooter.make,
                    "longitude": scooter.longitude,
                    "latitude": scooter.latitude,
                    "remaining_power": scooter.remaining_power,
                    "cost_per_time": scooter.cost_per_time,
                    "status": scooter.status,
                }
                scooters_list.append(scooter_dict)

            bookings = Booking.query.filter_by(user_id=request["customer_id"])
            bookings_list = []
            for booking in bookings:
                booking_dict = {
                    "id": booking.id,
                    "scooter_id": booking.scooter_id,
                    "date": booking.date.strftime("%a %d %b, %H:%M, %Y"),
                    "start_time": booking.start_time.strftime("%H:%M, %Y"),
                    "status": booking.status
                }
                bookings_list.append(booking_dict)

            data = {
                "scooters": scooters_list,
                "bookings": bookings_list
            }

            return data
    except RequestException as req_error:
        return {"status_code": 500, "error": f"{req_error}"}
    except ValueError as json_error:
        return {"status_code": 500, "error": f"JSON decoding error while processing response: {json_error}"}
    except Exception as error:
        return {"status_code":500, "error": f"An unexpected error occurred: {error}" }
    
@comms.action("make-booking", ["start"])
def make_booking(handler, request):
    try: 
        # json_data = json.dumps(request["data"])
        # headers = {"Content-Type": "application/json"}

        # url = f"{API_BASE_URL}/bookings"
        # response = requests.post(url, data=request["data"], timeout=5)

        # # mark scooter as occupied
        # response.raise_for_status()

        booking_data = request["data"]

        booking = Booking(user_id=booking_data["user_id"],
                scooter_id=booking_data["scooter_id"],
                date=booking_data["date"],
                start_time=booking_data["start_time"],
                end_time=booking_data["end_time"],
                status=booking_data["status"])
        
        with app.app_context():
            db.session.add(booking)
            db.session.commit()
            return {}
    except RequestException as req_error:
        return {"status_code":500,"error": f"{req_error}" }
    except ValueError as json_error:
        return {"status_code":500, "error": f"JSON decoding error while processing response: {json_error}" }
    except Exception as error:
        return {"status_code":500, "error": f"An unexpected error occurred: {error}" }

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
