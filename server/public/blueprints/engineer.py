from flask import Blueprint, request, jsonify
from blueprints.customer import send_message

engineer = Blueprint("engineer", __name__)


@engineer.route("/scooters")
def scooters():
    message = {
        'method': 'GET',
        'uri': '/scooters/damaged'
    }

    response = send_message(message)

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

    message = {
        'method': 'POST',
        'uri': '/scooter/fixed',
        'params': {
            'scooter_id': scooter_id,
            'repair_id': repair_id
        }
    }

    response = send_message(message)

    if "error" in response:
        if response["error"] == "Unauthorised":
            return jsonify(response), 500
        return jsonify(response), 500
    else:
        return jsonify(response), 200
