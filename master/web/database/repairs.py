from flask import Blueprint, jsonify
from master.database.models import Repairs, RepairStatus
from master.database.database_manager import db

repairs_api = Blueprint("repairs_api", __name__)

def get_all():
    """
    Get a list of all repair records.

    Returns:
        JSON response with a list of repair records or an error message if no records are found.
    """
    return [repair.as_json() for repair in Repairs.query.all()]

def get(repair_id):
    """
    Get a specific repair record by its ID.

    Args:
        repair_id (int): The ID of the repair record to retrieve.

    Returns:
        JSON response with the repair record or an error message if not found.
    """
    repair = Repairs.query.get(repair_id)
    if repair:
        result = {
            "repair_id": repair.id,
            "scooter_id": repair.scooter_id,
            "report": repair.report,
            "status": repair.status
        }
    return result

def get_by_scooter(scooter_id):
    """
    Get the first repair record for a specified scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter.

    Returns:
        JSON response with the first repair record for the specified scooter or an error message if not found.
    """
    repair = Repairs.query.filter_by(scooter_id=scooter_id).first()
    if repair:
        return repair.as_json()
    else:
        return jsonify({"message": "No repairs found for the specified scooter_id"}), 404

def post(scooter_id,report,status):
    """
    Add a new repair record.

    Returns:
        JSON response with the added repair record or an error message if the record could not be added.
    """
    new_repair = Repairs(
        scooter_id=scooter_id,
        report=report,
        status=status
    )

    db.session.add(new_repair)
    db.session.commit()
    return new_repair.as_json()

def update(repair_id, new_repair):
    """
    Update an existing repair record by its ID.

    Args:
        repair_id (int): The ID of the repair record to update.

    Returns:
        JSON response with the updated repair record or an error message if the record could not be updated.
    """
    repair = Repairs.query.get(repair_id)
    if repair:
        repair.scooter_id = new_repair["scooter_id"]
        repair.report = new_repair["report"]
        repair.status = new_repair["status"]

        db.session.commit()
        return repair.as_json()
    else:
        return jsonify({"message": "Repair not found"}), 404

def delete(repair_id):
    """
    Delete an existing repair record by its ID.

    Args:
        repair_id (int): The ID of the repair record to delete.

    Returns:
        JSON response with the deleted repair record or an error message if the record could not be deleted.
    """
    repair = Repairs.query.get(repair_id)
    if repair:
        db.session.delete(repair)
        db.session.commit()
        return repair.as_json()
    else:
        return jsonify({"message": "Repair not found"}), 404

def get_pending_repairs():
    """
    Get repair records based on their status.

    Args:
        status (str): The status of repairs to filter.

    Returns:
        JSON response with a list of repair records matching the given status or an error message if none are found.
    """
    repairs = Repairs.query.filter_by(status=RepairStatus.PENDING.value).all()

    result = [
        {
            "repair_id": repair.id,
            "scooter_id": repair.scooter_id,
            "report": repair.report,
            "status": repair.status
        }
        for repair in repairs
    ]

    return result

def update_status(repair_id, status):
    """
    Update an existing repair record by its ID.

    Args:
        repair_id (int): The ID of the repair record to update.

    Returns:
        JSON response with the updated repair record or an error message if the record could not be updated.
    """
    repair = Repairs.query.get(repair_id)
    if repair:
        repair.status = status

        db.session.commit()
        return repair.as_json()
    else:
        return None