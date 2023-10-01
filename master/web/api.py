"""
API Blueprint

"""
from requests.exceptions import RequestException, Timeout
from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
import requests
from constants import API_BASE_URL

api = Blueprint("api", __name__)

@api.route("/")
def root():
    """
    Root route.

    Returns:
        str: A greeting message.
    """
    return "Good morning, everyone!"

@api.route("/register", methods=["POST"])
def register():
    """
    Register a user.

    This route expects a JSON request with a "username" and "password" field.
    It hashes the password and sends a registration request to an external server.

    Returns:
        jsonify: A JSON response indicating the registration status.
    """
    try:
        data = request.json  # Get JSON data from the request
        username = data.get("username")
        password = data.get("password")

        # You should hash the password before sending it to the server
        hashed_password = sha256_crypt.hash(password)

        response = requests.post(f"{API_BASE_URL}/user", json={"username": username, "password": hashed_password}, timeout=10)

        return jsonify({"message": response["message"]})

    except RequestException as error:
        print(error)
        return jsonify({"error": "Registration failed"}), 500  # Return an error response

@api.route("/login", methods=["POST"])
def login_user():
    """
    Login a user.

    This route expects a JSON request with a "username" and "password" field.
    It sends a login request to an external server and verifies the user's credentials.

    Returns:
        jsonify: A JSON response indicating the login status and user type.
    """
    try:
        data = request.json  # Get JSON data from the request
        username = data.get("username")
        password = data.get("password")

        response = requests.get(f"{API_BASE_URL}/user/{username}", timeout=10)
        user_data = response.json()

        # Check if the username exists and verify the password
        if "password" in user_data and sha256_crypt.verify(password, user_data["password"]):
            # Send confirmation and user type to the agent
            return jsonify({"message": "Login successful", "user_type": user_data.get("user_type")})

        return jsonify({"error": "Login failed"}), 401  # Unauthorized

    except (RequestException, Timeout) as error:
        print(error)
        return jsonify({"error": "Login failed"}), 500  # Return an error response
