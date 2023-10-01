from flask import Blueprint, request, jsonify
from master.database.models import Transaction
from master.database.database_manager import db

transaction_api = Blueprint("transaction_api", __name__)

@transaction_api.route("/transactions", methods=["GET"])
def get_transactions():
    """
    Get a list of all transactions.

    Returns:
        JSON response with a list of transaction objects.
    """
    transactions = Transaction.query.all()
    result = [
        {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount
        }
        for transaction in transactions
    ]
    return jsonify(result)

@transaction_api.route("/transaction/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    """
    Get a transaction by its ID.

    Args:
        transaction_id (int): The ID of the transaction to retrieve.

    Returns:
        JSON response with the transaction object or a "Transaction not found" message.
    """
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        result = {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Transaction not found"}), 404

@transaction_api.route("/transactions", methods=["POST"])
def add_transaction():
    """
    Create a new transaction.

    Returns:
        JSON response with the newly created transaction object and a status code of 201.
    """
    data = request.json
    new_transaction = Transaction(
        user_id=data.get("user_id"),
        amount=data.get("amount")
    )

    db.session.add(new_transaction)
    db.session.commit()

    result = {
        "id": new_transaction.id,
        "user_id": new_transaction.user_id,
        "amount": new_transaction.amount
    }
    return jsonify(result), 201

@transaction_api.route("/transactions/user/<int:user_id>", methods=["GET"])
def get_transactions_by_user(user_id):
    """
    Get all transactions for a specific user by their user ID.

    Args:
        user_id (int): The ID of the user for whom to retrieve transactions.

    Returns:
        JSON response with a list of transaction objects for the specified user.
    """
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    result = [
        {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount
        }
        for transaction in transactions
    ]
    return jsonify(result)
