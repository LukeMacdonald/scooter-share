from flask import Blueprint, request, jsonify
from master.database.database_manager import db
from master.database.models import Scooter, ScooterStatus
import master.database.queries as queries

scooter_api = Blueprint("scooter_api", __name__)

@scooter_api.route("/scooters", methods=["GET"])
def get_all_scooters():
    """
    Get a list of all scooters.

    Returns:
        JSON response with a list of all scooter objects.
    """
    scooters = Scooter.query.all()
    return jsonify([scooter.as_json() for scooter in scooters])

@scooter_api.route("/scooters/<int:scooter_id>", methods=["GET"])
def get_scooter(scooter_id):
    """
    Get a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to retrieve.

    Returns:
        JSON response with the scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        return jsonify(result.as_json())
    else:
        return jsonify({'message': 'Scooter not found'}), 404

@scooter_api.route("/scooters/status/<string:status>", methods=["GET"])
def get_scooters_by_status(status):
    """
    Get a list of scooters by their status.

    Args:
        status (str): The status of the scooters to retrieve.

    Returns:
        JSON response with a list of scooters with the specified status.
    """
    if status not in [status.value for status in ScooterStatus]:
        return jsonify({'message': 'Invalid status provided'}), 400

    scooters = Scooter.query.filter_by(status=status).all()
    if scooters:
        return jsonify([scooter.as_json() for scooter in scooters])
    else:
        return jsonify({'message': 'No scooters found with the specified status'}), 404

@scooter_api.route("/scooters/<int:scooter_id>", methods=["PUT"])
def update_scooter(scooter_id):
    """
    Update a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to update.

    Returns:
        JSON response with the updated scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        data = request.get_json()
        scooter.make = data['Make']
        scooter.longitude = data['Longitude']
        scooter.latitude = data['Latitude']
        scooter.remaining_power = data['RemainingPower']
        scooter.cost_per_time = data['CostPerTime']
        scooter.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Scooter updated successfully'})
    else:
        return jsonify({'message': 'Scooter not found'}), 404

@scooter_api.route("/scooters/<int:scooter_id>", methods=["DELETE"])
def delete_scooter(scooter_id):
    """
    Delete a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to delete.

    Returns:
        JSON response with the deleted scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        db.session.delete(scooter)
        db.session.commit()
        return jsonify({'message': 'Scooter deleted successfully'})
    else:
        return jsonify({'message': 'Scooter not found'}), 404

@scooter_api.route("/scooters/awaiting-repairs", methods=["GET"])
def get_scooters_awaiting_repairs():
    """
    Get a list of scooters with the status set to "awaiting repair" and their first repair request with status "active" if available.

    Returns:
        JSON response with a list of scooters and their first repair request or a "No data found" message.
    """
    return jsonify(queries.scooters_awaiting_repairs())

@scooter_api.route("/scooters/fixed/<int:scooter_id>/<int:repair_id>", methods=["PUT"])
def scooter_fixed(scooter_id, repair_id):
    """
    Mark a scooter as fixed and complete the corresponding repair.

    Args:
        scooter_id (int): The ID of the scooter to mark as fixed.
        repair_id (int): The ID of the repair to complete.

    Returns:
        JSON response with a success message or error message if the scooter or repair is not found.
    """
    message, status = queries.fix_scooter(scooter_id, repair_id)
    return jsonify(message), status
