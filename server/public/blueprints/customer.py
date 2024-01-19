from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from common.client import Client

customer = Blueprint("customer", __name__)


def send_message(message: dict):
    client = Client(host='127.0.0.1', port=54321)
    return client.send_message(message)


@customer.route('/data/<int:user_id>')
def customer_data(user_id):
    message = {
        'method': 'GET',
        'uri': '/customer/dashboard',
        'params': {
            "customer_id": user_id,
        }
    }

    response = send_message(message)

    return jsonify(response)


@customer.route('/scooter/<int:scooter_id>')
def scooter_data(scooter_id):
    message = {
        'method': 'GET',
        'uri': '/scooter',
        'params': {
            'scooter_id': scooter_id
        }
    }

    response = send_message(message)

    return jsonify(response)


@customer.route('/book', methods=["POST"])
def make_booking():
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: post request for make-booking, returns homepage.
    """

    req = request.get_json()

    start_time = req.get('start_time')

    duration = int(req.get('duration'))

    user_id = req.get('user_id')

    scooter_id = req.get('scooter_id')

    # Combine the start time with today's date to create a datetime object
    start_datetime = datetime.combine(date.today(), datetime.strptime(start_time, "%H:%M").time())

    end_datetime = start_datetime + timedelta(minutes=duration)

    message = {
        'method': 'POST',
        'uri': '/booking/create',
        'params': {
            'booking_data': {

                "scooter_id": scooter_id,
                "user_id": user_id,
                "date": date.today().isoformat(),
                "start_time": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "active",
                "event_id": "0"

            }

        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400
    else:
        return jsonify(response), 201


@customer.route('/cancel-booking/<int:booking_id>', methods=["DELETE"])
def cancel_booking(booking_id):
    """
    Cancel a booking.

    Sends a request to cancel a booking to the server, removes the associated
    calendar event, and redirects the user to the customer home page.

    Args:
        booking_id (int): The ID of the booking to be canceled.

    Returns:
        Flask response: A JSON response indicating the success or failure of the cancellation.
    """

    message = {
        'method': 'UPDATE',
        'uri': '/booking/cancel',
        'params': {
            'booking_id': booking_id
        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 200


@customer.route('/report', methods=["POST"])
def report_issue():
    """
    Report an issue with a scooter.

    Sends a report issue request to the server for a specific scooter and redirects
    the user to the customer home page.

    Args:
        scooter_id (int): The ID of the scooter for which the issue is being reported.

    Returns:
        Flask response: A redirect response to the customer home page.
    """

    data = request.get_json()

    message = {
        'method': 'UPDATE',
        'uri': '/booking/cancel',
        'params': {
            'booking_id': data.get("booking_id")
        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400

    message = {
        'method': 'POST',
        'uri': '/scooter/damaged',
        'params': {
            'scooter_id': data.get("scooter_id"),
            'report': data.get("report")
        }

    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400
    else:
        # cal.remove(data.get("event_id"))
        return jsonify(response), 200


@customer.route('/top-up-balance', methods=["POST"])
def top_up_balance():
    """
    Display the page for topping up balance.

    Returns:
        Flask response: The top-up-balance page.
    """

    data = request.get_json()

    message = {
        'method': 'UPDATE',
        'uri': '/top-up',
        'params': {
            'user_id': int(data.get('user_id')),
            'amount': float(data.get("amount"))
        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400
    else:
        return jsonify(response), 200


@customer.route('/scooter/unlock/<int:scooter_id>/<int:user_id>', methods=["GET"])
def unlock_scooter(scooter_id, user_id):
    message = {
        'method': 'UPDATE',
        'uri': '/scooter/unlock',
        'params': {
            'user_id': int(user_id),
            'scooter_id': int(scooter_id)
        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 200


@customer.route('/scooter/lock/<int:scooter_id>/<int:user_id>', methods=["GET"])
def lock_scooter(scooter_id, user_id):
    message = {
        'method': 'UPDATE',
        'uri': '/scooter/lock',
        'params': {
            'user_id': int(user_id),
            'scooter_id': int(scooter_id)
        }
    }

    response = send_message(message)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 200
