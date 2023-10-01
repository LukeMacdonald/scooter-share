import requests
from passlib.hash import sha256_crypt
from requests.exceptions import RequestException
from master.agent_interface import comms
from agent_common import socket_utils
from database.models import User, UserType, Scooter, Booking
from database.database_manager import db
from flask import jsonify
from constants import API_BASE_URL
from credentials.email import send_email

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
                    "time": booking.time.strftime("%a %d %b, %H:%M, %Y"),
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
        url = "http://localhost:5000/bookings"
        response = requests.post(url, timeout=5, data=request["data"])

        # mark scooter as occupied
        response.raise_for_status()
        return {"status_code":response.status_code, "data": response.json()}
    except RequestException as req_error:
        return {"status_code":500,"error": f"{req_error}" }
    except ValueError as json_error:
        return {"status_code":500, "error": f"JSON decoding error while processing response: {json_error}" }
    except Exception as error:
        return {"status_code":500, "error": f"An unexpected error occurred: {error}" }

@comms.action("email-engineer", ["start"])
def email_engineer(handler, request):
    try:
        # Retrieve scooter information
        # scooter_id = request["scooter_id"]
        # report = request["repair_report"]
        scooter_id = 1
        report = "The scooters tires have gone flat"
        scooter_data = get_scooter_info(scooter_id)
        
        
        # Get scooter location
        latitude = scooter_data.get('Latitude')
        longitude = scooter_data.get('Longitude')
        formatted_address = get_formatted_address(latitude, longitude)
        
        # Get engineer emails
        engineer_emails = get_engineer_emails()
        
        # Send repair request to emails (currently set to just personal email to prevent sending emails to 
        # unknown addresses)
        send_repair_request_email(scooter_id,report,formatted_address,["lukemacdonald560@gmail.com"])
       
        
        return {"status_code": 200, "message": "Email sent successfully"}

    except RequestException as req_error:
        return {"status_code": 500, "error": f"Request error while updating scooter status: {req_error}"}

def get_scooter_info(scooter_id):
    scooter_url = f"{API_BASE_URL}/scooters/{scooter_id}"
    response = requests.get(scooter_url, timeout=5)
    return response.json()

def get_formatted_address(latitude, longitude):
    address_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&location_type=ROOFTOP&key=AIzaSyCI9KBPlHOzx9z7dp41LNbzpYaVn3qqgNY"
    response = requests.get(address_url, timeout=5)
    address_data = response.json()
    return address_data.get('results')[0].get('formatted_address')

def get_engineer_emails():
    engineer_emails_url = f"{API_BASE_URL}/engineer_emails"
    response = requests.get(engineer_emails_url, timeout=5)
    return response.json()

def send_repair_request_email(scooter_id,report, location, engineer_emails):
    email_subject = 'URGENT: Scooter Repair Request'
    email_body = f'''
        <html>
        <head>
            <style>
                /* CSS styles for the table */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{email_subject}</h2>
                </div>
                <div class="content">
                    <p><strong>Dear Engineers,</strong></p>
                    <p>We have received a report regarding a damaged scooter that requires immediate attention.</p>
                    <table>
                        <tr>
                            <th>Scooter ID</th>
                            <td>{scooter_id}</td>
                        </tr>
                        <tr>
                            <th>Issue Reported</th>
                            <td>{report}</td>
                        </tr>
                        <tr>
                            <th>Location</th>
                            <td>{location}</td>
                        </tr>
                    </table>
                    <p>Please review the situation and take necessary actions to address the issue as soon as possible.</p>
                    <p>Thank you for your prompt attention to this matter.</p>
                    <p>Best regards,</p>
                    <p><strong>Scooter Share Co</strong></p>
                </div>
            </div>
        </body>
        </html>
    '''

    # Send email to multiple engineers
    for email in engineer_emails:
        send_email(email_subject, email, email_body)

def run_agent_server(master):
    global app
    app = master
    comms.run(socket_utils.SOCKET_PORT)
