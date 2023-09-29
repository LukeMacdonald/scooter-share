from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from database.models import User, UserType
from database.database_manager import db

users_api = Blueprint("db_user", __name__)

@users_api.route("/users", methods=["GET"])
def get_users():
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    users = User.query.all()
    result = [
        {
            "id": user.id, 
            "username": user.username, 
            "email": user.email, 
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "role": user.role,
            "phone_number": user.phone_number,
            "balance": user.balance
        } 
        for user in users]
    return jsonify(result)

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
        result = {
            "id": user.id, 
            "username": user.username, 
            "email": user.email, 
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "role": user.role,
            "phone_number": user.phone_number,
            "balance": user.balance
        }
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"}), 404

@users_api.route("/users", methods=["POST"])
def add_user():
    """
    Create a new user.

    Returns:
        JSON response with the newly created user object and a status code of 201.
    """
    data = request.json
    password = data.get("password")
    
    if not password:
        return jsonify({"message": "Password is required"}), 400

    new_user = User(
        username=data.get("username"),
        password=password,
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        role=data.get("role"),
        phone_number=data.get("phone_number"),
        balance=data.get("balance")
    )

    db.session.add(new_user)
    db.session.commit()

    result = {
        "id": new_user.id, 
        "username": new_user.username, 
        "email": new_user.email, 
        "first_name": new_user.first_name, 
        "last_name": new_user.last_name,
        "role": new_user.role,
        "phone_number": new_user.phone_number,
        "balance": new_user.balance
    }
    return jsonify(result), 201

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

        result = {
            "id": user.id, 
            "username": user.username, 
            "email": user.email, 
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "role": user.role,
            "phone_number": user.phone_number,
            "balance": user.balance
        }
        return jsonify(result)
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
        result = {
            "id": user.id, 
            "username": user.username, 
            "email": user.email, 
            "first_name": user.first_name, 
            "last_name": user.last_name,
            "role": user.role,
            "phone_number": user.phone_number,
            "balance": user.balance
        }
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"}), 404

@users_api.route("/engineer_emails", methods=["GET"])
def get_engineer_emails():
    """
    Get email addresses of users with the "engineer" role.

    Returns:
        JSON response with a list of email addresses.
    """
    engineer_users = User.query.filter_by(role=UserType.ENGINEER.value).all()
    engineer_emails = [user.email for user in engineer_users]
    
    return jsonify(engineer_emails)