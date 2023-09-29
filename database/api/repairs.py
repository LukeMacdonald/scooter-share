from flask import Blueprint, request, jsonify
from database.models import Repairs
from database.database_manager import db

repairs_api = Blueprint("repairs_api", __name__)

@repairs_api.route("/repairs", methods=["GET"])
def get_repairs():
    """
    Get a list of all repair records.

    Returns:
        JSON response with a list of repair records or an error message if no records are found.
    """
    repairs = Repairs.query.all()
    result = [
        {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "status": repair.status
        }
        for repair in repairs
    ]
    return jsonify(result)

@repairs_api.route("/repair/<int:repair_id>", methods=["GET"])
def get_repair(repair_id):
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
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404

@repairs_api.route("/repairs/scooter/<int:scooter_id>", methods=["GET"])
def get_first_repair_by_scooter(scooter_id):
    """
    Get the first repair record for a specified scooter by its ID.

    Args:
        scooter_id (int): The ID of the scooter.

    Returns:
        JSON response with the first repair record for the specified scooter or an error message if not found.
    """
    repair = Repairs.query.filter_by(scooter_id=scooter_id).first()
    if repair:
        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "No repairs found for the specified ScooterID"}), 404

@repairs_api.route("/repairs", methods=["POST"])
def add_repair():
    """
    Add a new repair record.

    Returns:
        JSON response with the added repair record or an error message if the record could not be added.
    """
    data = request.json
    new_repair = Repairs(
        scooter_id=data.get("ScooterID"),
        report=data.get("Report"),
        status=data.get("status")
    )

    db.session.add(new_repair)
    db.session.commit()

    result = {
        "RepairID": new_repair.id,
        "ScooterID": new_repair.scooter_id,
        "Report": new_repair.report,
        "status": new_repair.status
    }
    return jsonify(result), 201

@repairs_api.route("/repair/<int:repair_id>", methods=["PUT"])
def update_repair(repair_id):
    """
    Update an existing repair record by its ID.

    Args:
        repair_id (int): The ID of the repair record to update.

    Returns:
        JSON response with the updated repair record or an error message if the record could not be updated.
    """
    repair = Repairs.query.get(repair_id)
    if repair:
        data = request.json
        repair.scooter_id = data.get("ScooterID")
        repair.report = data.get("Report")
        repair.status = data.get("status")

        db.session.commit()

        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404

@repairs_api.route("/repair/<int:repair_id>", methods=["DELETE"])
def delete_repair(repair_id):
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
        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404
