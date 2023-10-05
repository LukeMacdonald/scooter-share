from flask import Blueprint, jsonify
from master.database.database_manager import db
from master.database.models import Scooter, ScooterStatus
import master.database.queries as queries

scooter_api = Blueprint("scooter_api", __name__)

def post(data):
    """
    Create a new scooter record.

    Returns:
        JSON response with the newly created scooter object or an error message if the data is invalid.
    """
    
    make = data['make']
    longitude = data['longitude']
    latitude = data['latitude']
    remaining_power = 100.0
    cost_per_time = data['cost_per_time']
    colour = data['colour']
    status = ScooterStatus.AVAILABLE.value

    # Validate the required fields
    if not make or not longitude or not latitude or not remaining_power or not cost_per_time or not status:
        return jsonify({'message': 'Invalid data provided'}), 400

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
def get_all():
    """
    Get a list of all scooters.

    Returns:
        JSON response with a list of all scooter objects.
    """
    scooters = Scooter.query.all()
    return [scooter.as_json() for scooter in scooters]

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
        return jsonify({'message': 'Scooter not found'})

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

def update(scooter_id, data):
    """
    Update a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to update.

    Returns:
        JSON response with the updated scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        scooter.make = data.make
        scooter.longitude = data.longitude
        scooter.latitude = data.latitude
        scooter.remaining_power = data.remaining_power
        scooter.cost_per_time = data.cost_per_time
        scooter.status = data.status
        db.session.commit()
        return scooter.as_json()
     
    else:
        return None

def update_status(scooter_id, status):
    """
    Update a scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter to update.

    Returns:
        JSON response with the updated scooter object or a "Scooter not found" message.
    """
    scooter = Scooter.query.get(scooter_id)
    if scooter:
        scooter.status = status
        db.session.commit()
        return scooter.as_json()
     
    else:
        return None

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
        db.session.delete(scooter)
        db.session.commit()
        return jsonify({'message': 'Scooter deleted successfully'})
    else:
        return jsonify({'message': 'Scooter not found'}), 404

def get_scooters_awaiting_repairs():
    """
    Get a list of scooters with the status set to "awaiting repair" and their first repair request with status "active" if available.

    Returns:
        JSON response with a list of scooters and their first repair request or a "No data found" message.
    """
    return jsonify(queries.scooters_awaiting_repairs())

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
