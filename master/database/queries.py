from master.database.database_manager import db
from master.database.models import Repairs, RepairStatus, Scooter, ScooterStatus

def scooters_awaiting_repairs():
    # Use a subquery to find the first repair request with status "active" for each scooter with status "awaiting repair."
    subquery = db.session.query(
        Repairs.scooter_id,
        db.func.min(Repairs.id).label("repair_id")
    ).filter_by(status="active").group_by(Repairs.scooter_id).subquery()

    # Join the Scooter and Repairs tables using the subquery to fetch data.
    query = db.session.query(
        Scooter.id.label("scooter_id"),
        Scooter.make.label("make"),
        Scooter.longitude.label("longitude"),
        Scooter.latitude.label("latitude"),
        Scooter.remaining_power.label("remaining_power"),
        Scooter.cost_per_time.label("cost_per_time"),
        Scooter.status.label("scooter_status"),
        Repairs.report.label("report"),
        Repairs.status.label("repair_status"),
        subquery.c.repair_id.label("repair_id")
    ).join(
        subquery, Scooter.id == subquery.c.scooter_id, isouter=True
    ).join(
        Repairs, Repairs.id == subquery.c.repair_id, isouter=True
    )

    results = query.all()
    result_list = []
    for row in results:
        if row.scooter_status == ScooterStatus.AWAITING_REPAIR.value and row.repair_status == RepairStatus.ACTIVE.value:
            scooter_data = {
                "scooter_id": row.scooter_id,
                "make": row.make,
                "longitude": row.longitude,
                "latitude": row.latitude,
                "remaining_power": row.remaining_power,
                "cost_per_id": row.cost_per_time,
                "scooter_status": row.scooter_status,
                "repair_report": row.report,
                "repair_id": row.repair_id
            }
            result_list.append(scooter_data)
    return result_list

def fix_scooter(scooter_id, repair_id):
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
        return {'message': f'Scooter with ID {scooter_id} not found'}, 404
    elif repair is None:
        return {'message': f'Repair with ID {repair_id} not found'}, 404
    else:
        scooter.status = ScooterStatus.AVAILABLE.value
        repair.status = RepairStatus.COMPLETED.value
        db.session.commit()
        return {'message': 'Scooter successfully repaired'}, 200
