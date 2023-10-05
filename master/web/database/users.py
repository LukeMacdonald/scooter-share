from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from master.database.models import User, UserType
from master.database.database_manager import db

users_api = Blueprint("db_user", __name__)

@users_api.route("/users", methods=["GET"])
def get_users():
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    return jsonify([user.as_json() for user in User.query.all()])

@users_api.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        JSON response with the user object or a "User not found" message.
    """
    user = User.query.get(user_id)
    if user:
        return jsonify(user.as_json())
    else:
        return jsonify({"message": "User not found"}), 404

# @users_api.route("/users", methods=["POST"])
def add_user(data):
    """
    Create a new user.

    Returns:
        JSON response with the newly created user object and a status code of 201.
    """
    # data = request.json
    password = data.get("password")
    
    if not password:
        return jsonify({"message": "Password is required"}), 400
    
    if "balance" in data:
        balance = data["balance"]
    else:
        balance = 0.0

    new_user = User(
        username=data.get("username"),
        password=password,
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        role=data.get("role"),
        phone_number=data.get("phone_number"),
        balance=balance
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user.as_json()

@users_api.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.

    Returns:
        JSON response with the updated user object or a "User not found" message.
    """
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.username = data.get("username")
        user.email = data.get("email")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.role = data.get("role")
        user.phone_number = data.get("phone_number")
        user.balance = data.get("balance")

        db.session.commit()
        return jsonify(user.as_json())
    else:
        return jsonify({"message": "User not found"}), 404

@users_api.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        JSON response with the deleted user object or a "User not found" message.
    """
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.as_json())
    else:
        return jsonify({"message": "User not found"}), 404

def get_engineer_emails():
    """
    Get email addresses of users with the "engineer" role.

    Returns:
        JSON response with a list of email addresses.
    """
    engineer_users = User.query.filter_by(role=UserType.ENGINEER.value).all()
    engineer_emails = [user.email for user in engineer_users]
    
    return engineer_emails
