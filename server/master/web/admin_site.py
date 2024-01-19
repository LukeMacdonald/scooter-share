"""
Blueprint for Admin Routes

"""
import requests
from requests.exceptions import RequestException
from flask import Blueprint, request, jsonify
from comms import helpers
from database.models import RepairStatus, UserType, BookingState, ScooterStatus
from comms.utils import message_scooter

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_BASE_URL = "http://localhost:5000"

admin = Blueprint("admin", __name__)

@admin.route("/data")
def home():
    """
    Display the admin home page.

    Returns:
        Flask response: The admin home page.
    """
    scooters = requests.get(f"{API_BASE_URL}/scooters/all", timeout=5).json()
    customers = requests.get(f"{API_BASE_URL}/user/role/{UserType.CUSTOMER.value}", timeout=5).json()

    for scooter in scooters:
        scooter['location'] = helpers.get_street_address(scooter["latitude"], scooter["longitude"])

    data = {
        'scooters': scooters,
        'customers': customers
    }

    return jsonify(data), 200


@admin.route("/scooter/bookings")
def bookings():
    """
    Display the admin page for scooter bookings.

    Returns:
        Flask response: The scooter bookings page.
    """

    completed_bookings = requests.get(f"{API_BASE_URL}/bookings/status/{BookingState.COMPLETED.value}",
                                      timeout=5).json()

    for booking in completed_bookings:
        booking["start_time"] = helpers.convert_time_format(booking["start_time"])

    return jsonify(completed_bookings), 200


@admin.route("/scooters/usage")
def scooter_usage():
    """
    Display the admin page for scooter usage statistics.

    Returns:
        Flask response: The scooter usage statistics page.
    """
    completed_bookings = requests.get(f"{API_BASE_URL}/bookings/status/{BookingState.COMPLETED.value}",
                                      timeout=5).json()
    for booking in completed_bookings:
        booking["duration"] = helpers.calculate_duration(booking["start_time"], booking["end_time"])
        booking["start_time"] = helpers.convert_time_format(booking["start_time"])

    return jsonify(completed_bookings), 200


@admin.route("/customer/get/<int:user_id>")
def get_customer(user_id):
    """
    Edit customer information.

    Args:
        user_id (int): The unique identifier for the customer.

    Returns:
        str: Rendered template for editing user information.
    """
    response = requests.get(f"{API_BASE_URL}/user/id/{user_id}", timeout=5)
    customer = response.json()

    return jsonify(customer), 200


@admin.route("/customer/update", methods=['PUT'])
def update_customer():
    """
    Update customer information based on the form data.

    Returns:
        response: Redirect to the admin home page if successful, or error message with status code 500 if there is an error.
    """
    try:
        req = request.get_json()
        print(req);
        user_id = req.get('id')

        response = requests.get(f"{API_BASE_URL}/user/id/{user_id}", timeout=5)

        print(response.json())

        if response.status_code == 400:
            return jsonify({"error": "User Not Found"}), 404

        user = response.json()

        user["first_name"] = req.get('first_name')
        user["last_name"] = req.get('last_name')
        user["phone_number"] = req.get('phone_number')

        updated_user = requests.put(f"{API_BASE_URL}/user/{user_id}", json=user, timeout=5).json()

        return jsonify(updated_user), 200

    except RequestException as error:
        print(f"Error during API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/customer/delete/<int:user_id>")
def delete_customer(user_id):
    """
    Delete a customer record.

    Args:
        user_id (int): The unique identifier for the customer.

    Returns:
        response: Redirect to the admin home page if successful, or error message with status code 500 if there is an error.
    """
    try:
        # todo: Delete all entries of user in other tables aswell.

        requests.delete(f"{API_BASE_URL}/user/{user_id}", timeout=5).json()
        return jsonify({"message": "Account Deleted!"})

    except RequestException as error:
        print(f"Error during API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/scooter/get/<int:scooter_id>")
def get_scooter(scooter_id):
    """
    Delete a scooter record based on the provided scooter ID.

    Args:
        scooter_id (int): The unique identifier for the scooter to be deleted.

    Returns:
        response: Redirect to the admin home page if the deletion is successful.
                 If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:

        # todo: Delete all upcoming bookings with this scooter

        response = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5)
        scooter = response.json()
        return jsonify(scooter), 200

    except RequestException as error:
        print(f"Error during API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/scooter/update", methods=['PUT'])
def scooter_update():
    """
    Update scooter information based on the form data provided via a POST request.

    Returns:
        response: Redirect to the admin home page if the update is successful.
                 If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:
        req = request.get_json()
        scooter_id = req.get('scooter_id')
        response = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5)
        if response.status_code == 404:
            return {"error": "Scooter Not Found"}

        scooter = response.json()
        scooter["colour"] = req.get("colour")
        scooter["make"] = req.get('make')
        scooter["cost_per_time"] = float(req.get('cost_per_time'))
        scooter["remaining_power"] = float(req.get('remaining_power'))
        scooter["longitude"] = float(req.get('longitude'))
        scooter["latitude"] = float(req.get('latitude'))

        updated_scooter = requests.put(f"{API_BASE_URL}/scooter/id/{scooter_id}", json=scooter, timeout=5).json()

        return jsonify(updated_scooter), 200
    except RequestException as error:
        print(f"Error during API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/scooter/delete/<int:scooter_id>")
def delete_scooter(scooter_id):
    """
    Delete a scooter record based on the provided scooter ID.

    Args:
        scooter_id (int): The unique identifier for the scooter to be deleted.

    Returns:
        response: Redirect to the admin home page if the deletion is successful.
                 If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:

        # todo: Delete all upcoming bookings with this scooter

        requests.delete(f"{API_BASE_URL}/scooter/{scooter_id}", timeout=5).json()
        return jsonify({"message": "Scooter Deleted!"}), 200

    except RequestException as error:
        print(f"Error during API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/scooter/submit", methods=['POST'])
def submit_scooter():
    """
    Handle the submission of a new scooter based on the form data provided via a POST request.

    Returns:
        response: Redirect to the admin home page if the submission is successful.
    """

    req = request.get_json()
    data = {
        "make": req.get('make'),
        "cost_per_time": req.get('cost'),
        "colour": req.get('colour'),
        "latitude": req.get('latitude'),
        "longitude": req.get('longitude')
    }

    scooter = requests.post(f"{API_BASE_URL}/scooter", json=data, timeout=5).json()
    return jsonify(scooter), 200


@admin.route("/repairs")
def confirm_reports():
    """
    Endpoint to retrieve and display pending repair reports for admin confirmation.

    Returns:
        str: Rendered HTML template containing pending repair reports.
    """
    try:
        scooters = []
        repairs = requests.get(f"{API_BASE_URL}/repairs/pending", timeout=5).json()
        for repair in repairs:
            response = requests.get(f"{API_BASE_URL}/scooter/id/{repair['scooter_id']}", timeout=5)

            scooter = response.json()

            repair['longitude'] = scooter['longitude']
            repair['latitude'] = scooter['latitude']

            scooters.append(response.json())
        return jsonify({'repairs': repairs, 'scooters': scooters}), 200
    except RequestException as error:
        print(f"Error during repairs API request: {error}")
        return jsonify({"error": "Internal Server Error"}), 500


@admin.route("/scooter/report", methods=['POST'])
def report_scooter():
    """
    Endpoint to process scooter repair reports submitted by users.

    Returns:
        Response: Redirects admin to the confirm_reports endpoint after processing the report.
    """
    try:
        req = request.get_json()
        repair_id = req.get('repair_id')
        data = {"status": RepairStatus.ACTIVE.value}
        updated_repair = requests.put(f"{API_BASE_URL}/repair/status/{repair_id}", json=data, timeout=5).json()

        data = {"status": ScooterStatus.AWAITING_REPAIR.value}

        scooter = requests.put(f"{API_BASE_URL}/scooter/status/{updated_repair['scooter_id']}", json=data,
                               timeout=5).json()

        # Send notifications to engineers
        notify_engineers(updated_repair["scooter_id"], updated_repair["report"])

        return jsonify({'message': 'maintence request sent to engineers.'})

    except RequestException as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500


@admin.route("/admin/notify/<int:scooter_id>/<string:report>", methods=["GET"])
def notify_engineers(scooter_id, report):
    """
    Notifies engineers about a reported scooter repair request via email.
    """
    try:

        scooter = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5).json()

        steet_address = helpers.get_street_address(scooter["latitude"], scooter["longitude"])

        engineer_emails = requests.get(f"{API_BASE_URL}/users/engineers/emails", timeout=5).json()

        email_subject = 'URGENT: Scooter Repair Request'

        email_body = helpers.get_email_body(scooter_id, report, steet_address, email_subject)

        # Send the email
        # send_email(email_subject, engineer_emails, email_body)

        print("Sending Email");

        return jsonify({'message': "email sent successfully!"}), 200

    except RequestException as error:
        print(str(error))
        return jsonify({'error': "Email sending failed"}), 500


@admin.route("/scooter/location/<int:scooter_id>", methods=["GET"])
def scooter_location(scooter_id):

    res = message_scooter(scooter_id, {"method": "LOCATION"})

    return jsonify(res), 200


@admin.route("/scooter/lock/<int:scooter_id>", methods=["GET"])
def scooter_lock(scooter_id):

    res = message_scooter(scooter_id, {"method": "LOCK"})

    return jsonify(res), 200


@admin.route("/scooter/unlock/<int:scooter_id>", methods=["GET"])
def scooter_unlock(scooter_id):

    res = message_scooter(scooter_id, {"method": "UNLOCK"})

    return jsonify(res), 200
