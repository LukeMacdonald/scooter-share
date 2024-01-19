from flask import Blueprint, request, jsonify
from blueprints.customer import send_message

auth = Blueprint("auth", __name__)

def check_role(role):
    return role == "customer" or role == 'engineer' or role == 'admin'


@auth.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    email = req.get('email', '')  # If 'email' is not present, default to an empty string
    password = req.get('password', '')  # If 'password' is not present, default to an empty string

    data = {
        "method": 'GET',
        "uri": "/login",
        "params": {
            "email": email,
            "password": password,
        }
    }

    response = send_message(data)

    print(response)

    if "user" in response:
        if not check_role(response["user"]["role"]):
            error_message = "Invalid user role"
            return jsonify({"error": error_message}), 400

    else:
        if response["error"]:
            error_message = response["error"]
        else:
            error_message = "Unknown Error"

        return jsonify({"error": error_message}), 404

    return jsonify(response)


@auth.route("/signup", methods=["POST"])
def signup():
    """
    Handle the signup form submission.

    Extracts user data from the form and performs the signup process.
    """

    req = request.get_json()

    message = {
        "method": 'POST',
        "uri": "/register",
        "params": {
            "user": {
                'username': req.get('username'),
                'email': req.get('email'),
                'password': req.get('password'),
                'first_name': req.get('firstName'),
                'last_name': req.get('lastName'),
                'role': req.get('role'),
                'phone_number': req.get('phoneNumber'),
            }
        }
    }

    response = send_message(message)

    print(response)

    if "user" in response:
        if not check_role(response["user"]["role"]):
            error_message = "Invalid user role"
            return jsonify({"error": error_message}), 400
    else:
        error_message = response.get("error", "Signup failed. Please try again.")
        return jsonify({"error": error_message}), 404

    return jsonify(response)
