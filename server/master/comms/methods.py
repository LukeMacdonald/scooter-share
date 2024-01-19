import re
import requests
from passlib.hash import sha256_crypt
from database.models import RepairStatus, ScooterStatus, BookingState
from comms.utils import message_scooter
import database.queries as queries

import datetime

from web.database.bookings import BookingAPI
from web.database.scooters import ScooterAPI
from web.database.transactions import TransactionAPI
from web.database.users import UserAPI

API_BASE_URL = "http://localhost:5000"

get_functions = {}
post_functions = {}
update_functions = {}
delete_functions = {}

VALID_METHODS = ["GET", "POST", "UPDATE", "DELETE"]


def http_method_decorator(method, functions_dict):
    def decorator(key, param_types={}):
        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                # Check parameter types
                for param, param_type in param_types.items():
                    if param in kwargs and not isinstance(kwargs[param], param_type):
                        raise TypeError(
                            f"Invalid type for parameter '{param}'. Expected {param_type.__name__}, got {type(kwargs[param]).__name__}")

                # Execute the wrapped function
                result = func(*args, **kwargs)

                # Return the result of the wrapped function
                return result

            functions_dict[key] = inner_wrapper
            return inner_wrapper

        return wrapper

    return decorator


def get(key, param_types={}):
    return http_method_decorator("GET", get_functions)(key, param_types)


def post(key, param_types={}):
    return http_method_decorator("POST", post_functions)(key, param_types)


def update(key, param_types={}):
    return http_method_decorator("UPDATE", update_functions)(key, param_types)


def delete(key, param_types={}):
    return http_method_decorator("DELETE", delete_functions)(key, param_types)


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


@post("/register", {"user": dict})
def register(user: dict):
    try:
        email = user["email"]
        phone_number = user["phone_number"]

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(email_regex, email):
            raise ValueError("Invalid email address format.")

        response = get_request(f"/user/email/{email}", check_status=False)
        if response.status_code == 200:
            raise ValueError("Email address already registered.")

        phone_regex = r'^[0-9]{10}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("Invalid phone number format.")

        user = post_request("/user", json=user).json()

        return {"user": user, "response": "yes"}
    except ValueError as error:
        return {"error": str(error)}


@get("/login", {"email": str, "password": str})
def login(email: str, password: str):
    response = get_request(f"/user/email/{email}", check_status=False)

    if response.status_code == 404:
        return {"error": "Email not found."}

    user = response.json()

    if not sha256_crypt.verify(password, user["password"]):
        return {"error": "Password is incorrect."}

    return {"user": user}


@get("/scooters/damaged")
def fetch_reported_scooters():
    """
        Fetch a list of scooters reported for repair.

        Returns:
            dict: A dictionary containing the fetched data or an error message.
        """
    return {"data": queries.scooters_awaiting_repairs()}


@update("/scooter/fixed", {"scooter_id": int, "repair_id": int})
def update_status(scooter_id: int, repair_id: int):
    """
        Mark scooter as repaired by updating its status as available.

        Args:
            scooter_id (int): The ID of the scooter to update.
            repair_id (int): The ID of the repair associated with the scooter.

        Returns:
            dict: A dictionary containing the response data or an error message.
        """
    message, status = queries.fix_scooter(scooter_id, repair_id)
    if status == 200:
        return {"message": message}
    else:
        return {"error": status}


@get("/customer/dashboard", {"customer_id": int})
def fetch_available_scooters(customer_id: int):
    """
        Fetch a list of available scooters.

        Returns:
            dict: A dictionary containing the fetched data or an error message.
        """
    try:
        if not customer_id:
            raise ValueError("customer_id was not supplied.")

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


@post("/booking/create", {"booking_data": dict})
def make_booking(booking_data: dict):
    """
        Handles the booking creation and updates scooter status to 'OCCUPYING'.

        Args:
            booking_data:
            handler: The handler object.
            request (dict): The booking request data.

        Returns:
            dict: A dictionary containing the response message.
        """
    try:

        if booking_data is None:
            raise ValueError("Booking data not passed!")

        booking = post_request("/bookings", json=booking_data).json()
        scooter_id = booking.get("scooter_id")

        if scooter_id:
            data = {"status": ScooterStatus.BOOKED.value}
            response = put_request(f"/scooter/status/{scooter_id}", json=data)
            if response.status_code == 400 or response.status_code == 404:
                return {"error": response.json['message']}
            return {"message": "Booking successfully made"}
        else:
            raise ValueError("Invalid scooter ID in the booking data.")
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@update('/booking/cancel', {'booking_id': int})
def cancel_booking(booking_id: int):
    """
        Updates a booking to have the status 'cancelled' in the database.

        Returns:
            dict: A dictionary containing the response message.
        """
    try:

        data = {"status": BookingState.CANCELLED.value}
        response = put_request(f"/booking/status/{booking_id}", json=data)
        if response.status_code != 404:
            booking = response.json()
            scooter_id = booking["scooter_id"]

            data = {"status": ScooterStatus.AVAILABLE.value}
            response = put_request(f"/scooter/status/{scooter_id}", json=data)

            if response.status_code in [400, 404]:
                return {"error": response.json['message']}
            return {"message": "Booking successfully cancelled"}
        else:
            return {"error": "Booking not found."}
    except Exception as e:
        return {"error": str(e)}


@post('/scooter/damaged', {'scooter_id': int, 'report': str})
def submit_repair_request(scooter_id: int, report: str):
    """
        Updates a scooter to have the status 'awaiting-repair' in the database.

        Returns:
            dict: A dictionary containing the response message.
        """
    try:
        if scooter_id is None:
            raise ValueError("ScooteID not passed!")

        if report is None:
            raise ValueError("Report Details Not Passed!")

        data = {
            "scooter_id": scooter_id,
            "report": report,
            "status": RepairStatus.PENDING.value
        }

        response = post_request("/repair", json=data)

        if response.status_code in [400, 404]:
            return {"error": response.json['message']}

        data = {"status": ScooterStatus.UNAVAILABLE.value}

        response = put_request(f"/scooter/status/{scooter_id}", json=data)
        if response.status_code in [400, 404]:
            return {"error": response.json['message']}

        return {"message": "Repair request submitted successfully."}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@update('/top-up', {'user_id': int, 'amount': float})
def top_up_balance(user_id: int, amount: float):
    """
        Updates the balance of a user.

        Returns:
            dict: An empty dictionary if no errors occured.
        """
    try:
        response = get_request(f"/user/id/{user_id}")
        if response.status_code == 404:
            raise ValueError("User not found")
        user = response.json()
        user["balance"] += amount

        response = put_request(f"/user/{user_id}", json=user, check_status=False)
        if response.status_code == 404:
            raise ValueError("Update user failed!")

        data = {"user_id": user_id, "amount": amount}
        post_request("/transaction", json=data)
        return {"new_balance": user["balance"]}
    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@get('/scooter', {'scooter_id': int})
def fetch_scooters_by_id(scooter_id: int):
    """
        Fetch a list of scooters.

        Returns:
            dict: A dictionary containing the fetched data or an error message.
        """
    try:

        if scooter_id is None:
            raise ValueError("ScooterID not found passed!")

        scooters = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5).json()
        data = scooters

        return data

    except ValueError as error:
        return {"error": str(error)}
    except Exception as error:
        return {"error": str(error)}


@update('/scooter/unlock', {'scooter_id': int, 'user_id': int})
def unlock_scooter(scooter_id: int, user_id: int):

    # Send message to scooter to unlock
    message_scooter(scooter_id, {'method': 'UNLOCK'})

    # Update Scooter Status to Occupying
    scooter = ScooterAPI.get(scooter_id)
    scooter['status'] = ScooterStatus.OCCUPYING.value
    ScooterAPI.update(scooter_id, scooter)

    # Get Details of Current Booking
    booking = BookingAPI.get_by_user_and_scooter(user_id=user_id, scooter_id=scooter_id)

    # Mark the proper first start time used for cost calculation
    booking.start_time = datetime.datetime.now()

    BookingAPI.update(booking.id, booking)

    return {"message": "Scooter Successfully Unlocked"}


@update('/scooter/lock', {'scooter_id': int, 'user_id': int})
def lock_scooter(scooter_id: int, user_id: int):

    message_scooter(scooter_id, {'method': 'UNLOCK'})

    booking = BookingAPI.get_by_user_and_scooter(user_id=user_id, scooter_id=scooter_id)

    # Update Booking
    booking.end_time = datetime.datetime.now()
    booking.status = BookingState.COMPLETED.value

    updated_booking = BookingAPI.update(booking.id, booking)

    # Get Scooter Information
    scooter = ScooterAPI.get(scooter_id)

    # Update Scooter
    location = message_scooter(scooter_id, {'method': 'LOCATION'})

    scooter['status'] = ScooterStatus.AVAILABLE.value
    scooter['longitude'] = float(location['lng'])
    scooter['latitude'] = float(location['lat'])

    ScooterAPI.update(scooter_id, scooter)

    # Calculate Ride Cose
    duration = (updated_booking.end_time - updated_booking.start_time).total_seconds() / 60

    cost = duration * (scooter['cost_per_time'] / 60)

    rounded_cost = round(cost, 2)

    TransactionAPI.create({'user_id': user_id, 'amount': rounded_cost})

    # Update User Balance

    user = UserAPI.get_by_id(user_id)

    user['balance'] = user['balance'] - rounded_cost

    UserAPI.update(user_id,user)

    return {"message": "Scooter Successfully Returned"}


@update('/scooter/repair', {'scooter_id': int})
def request_repair(scooter_id: int):
    scooter_update = {'status': ScooterStatus.AWAITING_REPAIR.value}
    requests.put(f"{API_BASE_URL}/scooter/status/{scooter_id}", json=scooter_update, timeout=5).json()
    return {"message": "Scooter Waiting for Repair"}


@get('/customer/bookings', {'user_id': int})
def check_booking(user_id: int):
    response = requests.get(f"{API_BASE_URL}/booking/user/{user_id}")
    if response.status_code == 404:
        return {'message': 'You don\'t have any bookings'}
    if response['user_id'] != user_id:
        return {'message': 'This scooter isn\'t booked by you'}
    else:
        return {'message': 'Unlocking Scooter'}


@get("/user", {'email': str})
def get_user(email: str):
    response = requests.get(f"{API_BASE_URL}/user/email/{email}")
    if response.status_code == 404:
        return {'message': 'invalid email', 'user_id': 0}
    else:
        response = response.json()
        print(response)
        return {'message': 'user found', 'user_id': response['id']}
