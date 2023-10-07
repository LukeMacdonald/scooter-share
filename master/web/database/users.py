from flask import Blueprint, jsonify, request
from master.database.models import User, UserType, Booking, Transaction
from master.database.database_manager import db

users_api = Blueprint("db_user", __name__)

@users_api.route("/users", methods=["GET"])
def get_all():
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    return [user.as_json() for user in User.query.all()]

@users_api.route("/user/role/<string:role>", methods=["GET"])
def get_all_by_role(role):
    """
    Get a list of all users.

    Returns:
        JSON response with a list of user objects.
    """
    users = User.query.filter_by(role=role).all()
    return [user.as_json() for user in users]

@users_api.route("/user/id/<int:user_id>", methods=["GET"])
def get(user_id):
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        JSON response with the user object or a "User not found" message.
    """
    
    user = User.query.get(user_id)
    if user:
        return user.as_json()
    else:
        return jsonify({"message": "User not found"}), 404

@users_api.route("/user", methods=["POST"])
def post():
    """
    Create a new user.

    Returns:
        JSON response with the newly created user object and a status code of 201.
    """
    data = request.json
    password = data["password"]
    
    if not password:
        return {"message": "Password is required"}
    
    if "balance" in data:
        balance = data["balance"]
    else:
        balance = 0.0

    new_user = User(
        username=data["username"],
        password=password,
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        role=data["role"],
        phone_number=data["phone_number"],
        balance=balance
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user.as_json()

@users_api.route("/user/<int:user_id>", methods=["PUT"])
def update(user_id):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.

    Returns:
        JSON response with the updated user object or a "User not found" message.
    """
    data = request.json
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
        return jsonify({"message": "User not found"}), 404

@users_api.route("/user/<int:user_id>", methods=["DELETE"])
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
        Booking.query.filter_by(user_id=user_id).delete()
        Transaction.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.as_json())
    else:
        return jsonify({"message": "User not found"}), 404

@users_api.route("/users/engineers/emails", methods=["GET"])
def get_engineer_emails():
    """
    Get email addresses of users with the "engineer" role.

    Returns:
        JSON response with a list of email addresses.
    """
    engineer_users = get_all_by_role(UserType.ENGINEER.value)
    engineer_emails = [user["email"] for user in engineer_users]
    
    return engineer_emails

@users_api.route("/user/email/<string:email>", methods=["GET"])
def get_by_email(email):
    user = User.query.filter_by(email=email).first() 
    if user:
        return user.as_json()
    return jsonify({"message": "User not found"}), 404