from flask import Blueprint, jsonify, request
from database.database_manager import db
from database.models import Scooter, ScooterStatus, Repairs, Booking
import database.queries as queries

scooter_api = Blueprint("scooter_api", __name__)

@scooter_api.route("/scooter", methods=["POST"])
def post():
    """
    Create a new scooter record.

    Returns:
        JSON response with the newly created scooter object or an error message if the data is invalid.
    """
    data = request.json
   

    # Validate the required fields
    if 'make' not in data or 'longitude' not in data or 'latitude' not in data or 'remaining_power' not in data or 'cost_per_time' not in data or 'status' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    make = data['make']
    longitude = data['longitude']
    latitude = data['latitude']
    remaining_power = 100.0
    cost_per_time = data['cost_per_time']
    colour = data['colour']
    status = ScooterStatus.AVAILABLE.value

    # Create a new scooter object
    new_scooter = Scooter(
        make=make,
        longitude=longitude,
        latitude=latitude,
        remaining_power=remaining_power,
        cost_per_time=cost_per_time,
        status=status,
        colour=colour
    )

    # Add the new scooter to the database
    db.session.add(new_scooter)
    db.session.commit()

    return new_scooter.as_json(), 201

@scooter_api.route("/scooters/all", methods=["GET"])
def get_all():
    """
    Get a list of all scooters.

    Returns:
        JSON response with a list of all scooter objects.
    """
    scooters = Scooter.query.all()
    return [scooter.as_json() for scooter in scooters]

@scooter_api.route("/scooter/id/<int:scooter_id>", methods=["GET"])
def get(scooter_id):
    """
    Get a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to retrieve.

    Returns:
        JSON response with the scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        return scooter.as_json()
    else:
        return jsonify({'message': 'Scooter not found'}), 404

@scooter_api.route("/scooters/status/<string:status>", methods=["GET"])
def get_by_status(status):
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
        
        return [scooter.as_json() for scooter in scooters]
    else:
        return []

@scooter_api.route("/scooter/id/<int:scooter_id>", methods=["PUT"])
def update(scooter_id):
    """
    Update a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to update.

    Returns:
        JSON response with the updated scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    data = request.json
    if scooter:
        scooter.make = data["make"]
        scooter.longitude = data["longitude"]
        scooter.latitude = data["latitude"]
        scooter.remaining_power = data["remaining_power"]
        scooter.cost_per_time = data["cost_per_time"]
        scooter.colour = data["colour"]
        scooter.status = data["status"]
        db.session.commit()
        return scooter.as_json()
     
    else:
        return jsonify({"message": "Scooter not found"}), 404

@scooter_api.route("/scooter/status/<int:scooter_id>", methods=["PUT"])
def update_status(scooter_id):
    """
    Update a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to update.

    Returns:
        JSON response with the updated scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    data = request.json
    
    # Validate the 'status' field against ScooterStatus enum
    if 'status' in data and data['status'] not in [status.value for status in ScooterStatus]:
        return jsonify({'message': 'Invalid status provided'}), 400
    if scooter:
        scooter.status = data["status"]
        db.session.commit()
        return scooter.as_json()
     
    else:
        return jsonify({"message": "Scooter not found"}), 404

@scooter_api.route("/scooter/<int:scooter_id>", methods=["DELETE"])
def delete(scooter_id):
    """
    Delete a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to delete.

    Returns:
        JSON response with the deleted scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        Booking.query.filter_by(scooter_id=scooter_id).delete()
        Repairs.query.filter_by(scooter_id=scooter_id).delete()
        db.session.delete(scooter)
        db.session.commit()
        return jsonify({'message': 'Scooter deleted successfully'})
    else:
        return jsonify({'message': 'Scooter not found'}), 404

@scooter_api.route("/scooters/awaiting", methods=["GET"])
def get_scooters_awaiting_repairs():
    """
    Get a list of scooters with the status set to "awaiting repair" and their first repair request with status "active" if available.

    Returns:
        JSON response with a list of scooters and their first repair request or a "No data found" message.
    """
    return jsonify(queries.scooters_awaiting_repairs())

@scooter_api.route("/scooter/fixed/<int:scooter_id>/<int:repair_id>", methods=["GET"])
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
