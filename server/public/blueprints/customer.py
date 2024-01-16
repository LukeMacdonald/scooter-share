from datetime import datetime, date, timedelta
from flask import Blueprint,request, jsonify
from connection import get_connection

customer = Blueprint("customer", __name__)

@customer.route('/data/<int:user_id>')
def customer_data(user_id):
    
    data = {
        "customer_id": user_id,
        "name": "customer-homepage"
    }
    
    response = get_connection().send(data)
            

    return jsonify(response)

@customer.route('/scooter/<int:scooter_id>')
def scooter_data(scooter_id):
    
    data = {
        "scooter_id": scooter_id,
        "name": "get-scooter-by-id"
    }
    
    response = get_connection().send(data)
    return jsonify(response)


@customer.route('/book', methods=["POST"])
def make_booking():
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: post request for make-booking, returns homepage.
    """
    
    req = request.get_json()
    
    print(req)

    start_time = req.get('start_time')
    
    duration = int(req.get('duration'))
    
    user_id = req.get('user_id')
    
    scooter_id = req.get('scooter_id')
   
    # Combine the start time with today's date to create a datetime object
    start_datetime = datetime.combine(date.today(), datetime.strptime(start_time, "%H:%M").time())
        
    end_datetime = start_datetime + timedelta(minutes=duration)

    data = {
        "data": {
        "scooter_id": scooter_id,
        "user_id": user_id,
        "date": date.today().isoformat(),
        "start_time": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "event_id": "0"
        },
        "name": "make-booking"
    }

    response = get_connection().send(data)
    if "error" in response:
        return jsonify(response), 400
    else:
        return jsonify(response), 201


from flask import request, jsonify

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
    response = get_connection().send({"name": "cancel-booking", "booking-id": booking_id})

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
    
    response = get_connection().send({"name" : "cancel-booking", "booking-id" : data.get("booking_id")})
    if "error" in response:
        return jsonify(response), 400
    
    response = get_connection().send({"name" : "report-issue", "scooter-id" : data.get("scooter_id"), "report": data.get("report")})
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
    
    response = get_connection().send({"user-id": data.get('user_id'), 
                                      "amount": data.get("amount"), "name": "top-up-balance"})
    if "error" in response:
        return jsonify(response), 400
    else:
        return jsonify(response), 200
    