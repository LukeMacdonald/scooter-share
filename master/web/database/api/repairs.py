from flask import Blueprint, request, jsonify
from master.web.database.models import Repairs
from master.web.database.database_manager import db

repairs_api = Blueprint("repairs_api", __name__)

@repairs_api.route("/repairs", methods=["GET"])
def get_repairs():
    repairs = Repairs.query.all()
    result = [
        {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "Status": repair.status
        }
        for repair in repairs
    ]
    return jsonify(result)

@repairs_api.route("/repair/<int:repair_id>", methods=["GET"])
def get_repair(repair_id):
    repair = Repairs.query.get(repair_id)
    if repair:
        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "Status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404

@repairs_api.route("/repairs/scooter/<int:scooter_id>", methods=["GET"])
def get_first_repair_by_scooter(scooter_id):
    repair = Repairs.query.filter_by(scooter_id=scooter_id).first()
    if repair:
        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "Status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "No repairs found for the specified ScooterID"}), 404

@repairs_api.route("/repairs", methods=["POST"])
def add_repair():
    data = request.json
    new_repair = Repairs(
        scooter_id=data.get("ScooterID"),
        report=data.get("Report"),
        status=data.get("Status")
    )

    db.session.add(new_repair)
    db.session.commit()

    result = {
        "RepairID": new_repair.id,
        "ScooterID": new_repair.scooter_id,
        "Report": new_repair.report,
        "Status": new_repair.status
    }
    return jsonify(result), 201

@repairs_api.route("/repair/<int:repair_id>", methods=["PUT"])
def update_repair(repair_id):
    repair = Repairs.query.get(repair_id)
    if repair:
        data = request.json
        repair.scooter_id = data.get("ScooterID")
        repair.report = data.get("Report")
        repair.status = data.get("Status")

        db.session.commit()

        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "Status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404

@repairs_api.route("/repair/<int:repair_id>", methods=["DELETE"])
def delete_repair(repair_id):
    repair = Repairs.query.get(repair_id)
    if repair:
        db.session.delete(repair)
        db.session.commit()
        result = {
            "RepairID": repair.id,
            "ScooterID": repair.scooter_id,
            "Report": repair.report,
            "Status": repair.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Repair not found"}), 404