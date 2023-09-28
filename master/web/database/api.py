"""
Database API Blueprint

This blueprint defines routes for interacting with the user database.
It provides endpoints for retrieving, adding, updating, and deleting user records.

"""
from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from master.web.database.models import User
from master.web.database.database_manager import db


db_api = Blueprint("db_api", __name__)

# Endpoint to show all users.
@db_api.route("/user", methods=["GET"])
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
            "role": user.role
        } 
        for user in users]
    return jsonify(result)

# Endpoint to get user by id.
@db_api.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a user by their ID.

    Args:
        id (int): The ID of the user to retrieve.

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
            "role": user.role
        }
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"}), 404

# Endpoint to create a new user.
@db_api.route("/user", methods=["POST"])
def add_user():
    """
    Create a new user.

    Returns:
        JSON response with the newly created user object and a status code of 201.
    """
    data = request.json
    password_hash = sha256_crypt.hash(data.get("password"))
    new_user = User(
        username=data.get("username"),
        password=password_hash,
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        role=data.get("role")  # Include the usertype in the creation
    )

    db.session.add(new_user)
    db.session.commit()

    result = {
        "id": new_user.id, 
        "username": new_user.username, 
        "email": new_user.email, 
        "first_name": new_user.first_name, 
        "last_name": new_user.last_name,
        "role": new_user.role  # Include the usertype in the response
    }
    return jsonify(result), 201

# Endpoint to update user.
@db_api.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user by their ID.

    Args:
        id (int): The ID of the user to update.

    Returns:
        JSON response with the updated user object or a "User not found" message.
    """
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.username = data.get("username")
        user.password = sha256_crypt.hash(data.get("password"))
        user.email = data.get("email")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")

        db.session.commit()

        result = {
            "id": user.id, 
            "username": user.username, 
            "email": user.email, 
            "first_name": user.first_name, 
            "last_name": user.last_name
        }
      
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"}), 404

# Endpoint to delete user.
@db_api.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by their ID.

    Args:
        id (int): The ID of the user to delete.

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
            "last_name": user.last_name
        }
        return jsonify(result)
    else:
        return jsonify({"message": "User not found"}), 404