from flask import Blueprint, request, jsonify
from master.web.database.models import Scooter
from master.web.database.database_manager import db

scooter_api = Blueprint("scooter_api", __name__)

@scooter_api.route("/scooters", methods=["GET"])
def get_all_scooters():
    """
    Get a list of all scooters.

    Returns:
        JSON response with a list of all scooter objects.
    """
    scooters = Scooter.query.all()
    result = [
        {
            'ScooterID': scooter.scooter_id,
            'Make': scooter.make,
            'Longitude': scooter.longitude,
            'Latitude': scooter.latitude,
            'RemainingPower': scooter.remaining_power,
            'CostPerTime': scooter.cost_per_time,
            'Status': scooter.status
        }
        for scooter in scooters
    ]
    return jsonify(result)

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
        result = {
            'ScooterID': scooter.scooter_id,
            'Make': scooter.make,
            'Longitude': scooter.longitude,
            'Latitude': scooter.latitude,
            'RemainingPower': scooter.remaining_power,
            'CostPerTime': scooter.cost_per_time,
            'Status': scooter.status
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Scooter not found'}), 404

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
        scooter.status = data['Status']
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
