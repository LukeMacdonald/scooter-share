from datetime import datetime, date, timedelta
from flask import Blueprint,request, jsonify
from connection import get_connection

customer = Blueprint("customer", __name__)

def convert_time_format(time_string):
    """
    Convert time string to a different format.
    """
    time_obj = datetime.strptime(time_string, "%a %d %b, %H:%M, %Y")
    return time_obj.strftime("%I:%M %p")


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
    
    print(response)
    
    return jsonify(response)
    