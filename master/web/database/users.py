from flask import Blueprint, jsonify
from master.database.models import User, UserType
from master.database.database_manager import db

users_api = Blueprint("db_user", __name__)

def get_all():
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    return [user.as_json() for user in User.query.all()]

def get_all_by_role(role):
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    users = User.query.filter_by(role=role).all()
    return [user.as_json() for user in users]

def get(user_id):
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        JSON response with the user object or a "User not found" message.
    """
    
    user = User.query.get(user_id)
    
    print(user.as_json()) 
    if user:
        return user.as_json()
    else:
        return None

def post(data):
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

def update(user_id, data):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.

    Returns:
        JSON response with the updated user object or a "User not found" message.
    """
    user = User.query.get(user_id) 
    if user:
       
        user.username = data["username"]
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.role = data["role"]
        user.phone_number = data["phone_number"]
        user.balance = data["balance"]

        db.session.commit()
        
        return user.as_json()
    else:
        return None

def delete(user_id):
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
    engineer_users = get_all_by_role(UserType.ENGINEER.value)
    engineer_emails = [user["email"] for user in engineer_users]
    
    return engineer_emails

def get_by_email(email):
    return User.query.filter_by(email=email).first()