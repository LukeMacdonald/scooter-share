from flask import Blueprint, jsonify
from master.database.models import Transaction
from master.database.database_manager import db

transaction_api = Blueprint("transaction_api", __name__)

def get_all():
    """
    Get a list of all transactions.

    Returns:
        JSON response with a list of transaction objects.
    """
    return jsonify([transaction.as_json() for transaction in Transaction.query.all()])

def get(transaction_id):
    """
    Get a transaction by its ID.

    Args:
        transaction_id (int): The ID of the transaction to retrieve.

    Returns:
        JSON response with the transaction object or a "Transaction not found" message.
    """
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        return jsonify(transaction.as_json())
    else:
        return jsonify({"message": "Transaction not found"}), 404

def post(user_id, amount):
    """
    Create a new transaction.

    Returns:
        JSON response with the newly created transaction object and a status code of 201.
    """
    new_transaction = Transaction(
        user_id=user_id,
        amount=amount
    )

    db.session.add(new_transaction)
    db.session.commit()
    return new_transaction.as_json()

def get_by_user(user_id):
    """
    Get all transactions for a specific user by their user ID.

    Args:
        user_id (int): The ID of the user for whom to retrieve transactions.

    Returns:
        JSON response with a list of transaction objects for the specified user.
    """
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([transaction.as_json() for transaction in transactions])
