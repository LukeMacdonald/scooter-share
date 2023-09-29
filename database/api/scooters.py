from flask import Blueprint, request, jsonify
from database.models import Scooter, ScooterStatus, Repairs, RepairStatus
from database.database_manager import db

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
            'ScooterID': scooter.id,
            'Make': scooter.make,
            'Longitude': scooter.longitude,
            'Latitude': scooter.latitude,
            'RemainingPower': scooter.remaining_power,
            'CostPerTime': scooter.cost_per_time,
            'status': scooter.status
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
            'ScooterID': scooter.id,
            'Make': scooter.make,
            'Longitude': scooter.longitude,
            'Latitude': scooter.latitude,
            'RemainingPower': scooter.remaining_power,
            'CostPerTime': scooter.cost_per_time,
            'status': scooter.status
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
    # Use a subquery to find the first repair request with status "active" for each scooter with status "awaiting repair."
    subquery = db.session.query(
        Repairs.scooter_id,
        db.func.min(Repairs.id).label("repair_id")
    ).filter_by(status="active").group_by(Repairs.scooter_id).subquery()

    # Join the Scooter and Repairs tables using the subquery to fetch data.
    query = db.session.query(
        Scooter.id.label("ScooterID"),
        Scooter.make.label("Make"),
        Scooter.longitude.label("Longitude"),
        Scooter.latitude.label("Latitude"),
        Scooter.remaining_power.label("RemainingPower"),
        Scooter.cost_per_time.label("CostPerTime"),
        Scooter.status.label("ScooterStatus"),
        Repairs.report.label("Report"),
        Repairs.status.label("RepairStatus"),
        subquery.c.repair_id.label("RepairID")
    ).join(
        subquery, Scooter.id == subquery.c.scooter_id, isouter=True
    ).join(
        Repairs, Repairs.id == subquery.c.repair_id, isouter=True
    )

    results = query.all()

    if results:
        result_list = []
        for row in results:
            if row.ScooterStatus == ScooterStatus.AWAITING_REPAIR.value and row.RepairStatus == "active":
                scooter_data = {
                    "ScooterID": row.ScooterID,
                    "Make": row.Make,
                    "Longitude": row.Longitude,
                    "Latitude": row.Latitude,
                    "RemainingPower": row.RemainingPower,
                    "CostPerTime": row.CostPerTime,
                    "ScooterStatus": row.ScooterStatus,
                    "RepairReport": row.Report,
                    "RepairID": row.RepairID
                }
                result_list.append(scooter_data)

        return jsonify(result_list)
    else:
        return jsonify({"message": "No data found"}), 404

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
    scooter = Scooter.query.get(scooter_id)
    repair = Repairs.query.get(repair_id)
    
    if scooter is None:
        return jsonify({'message': f'Scooter with ID {scooter_id} not found'}), 404
    elif repair is None:
        return jsonify({'message': f'Repair with ID {repair_id} not found'}), 404
    else:
        scooter.status = ScooterStatus.AVAILABLE.value
        repair.status = RepairStatus.COMPLETED.value
        db.session.commit()
        return jsonify({'message': 'Scooter successfully repaired'})
