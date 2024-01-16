from flask import Blueprint,request, jsonify
from connection import get_connection

engineer = Blueprint("engineer", __name__)

@engineer.route("/scooters")
def scooters():
    
    data = {"name": "locations"}
    response = get_connection().send(data)
    
    if "error" in response:
        return jsonify(response), 500

    return jsonify(response["data"]), 200


@engineer.route("/fixed", methods=["POST"])
def scooter_fixed():
    """
    Handle the scooter fixed form submission for engineers.

    Returns:
        Flask redirect: Redirects back to the update repair report page.
    """
    
    req = request.get_json()
    
    scooter_id = req.get("scooter_id")
    repair_id = req.get("repair_id")
    data = {"name": "repair-fixed", "scooter_id": scooter_id, "repair_id": repair_id}
    
    response = get_connection().send(data)
    
    if "error" in response:
        if response["error"] == "Unauthorised":
            
            return jsonify(response), 500
        return jsonify(response), 500
    else:
        return jsonify(response), 200