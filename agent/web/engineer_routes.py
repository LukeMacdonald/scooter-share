"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
from flask import Blueprint, render_template, url_for, redirect, request
from agent.web.connection import get_connection
from agent.web.login import eng_login_req

engineer = Blueprint("engineer", __name__)

@engineer.route("/engineer")
@eng_login_req
def home():
    """
    Display the engineer home page.

    Returns:
        Flask response: The engineer home page.
    """

    data = {"name": "locations"}
    response = get_connection().send(data)
    if "error" in response:
        redirect(url_for('user.logout'))
    else:
        return render_template("engineer/pages/home.html", scooter_data=response["data"])


@engineer.route("/engineer/scooters/locations")
@eng_login_req
def scooter_locations():
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """

    data = {"name": "locations"}
    response = get_connection().send(data)
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return render_template("engineer/pages/locations.html", scooter_data=response["data"])

@engineer.route("/engineer/scooters/repairs")
@eng_login_req
def update_report():
    """
    Display the update repair report page for engineers.

    Returns:
        Flask response: The update repair report page.
    """
    
    data = {"name": "locations"}
    response = get_connection().send(data)
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return render_template("engineer/pages/update_repair.html", scooter_data=response["data"])


@engineer.route("/engineer/scooter/fixed", methods=["POST"])
@eng_login_req
def scooter_fixed():
    """
    Handle the scooter fixed form submission for engineers.

    Returns:
        Flask redirect: Redirects back to the update repair report page.
    """
    
    scooter_id = request.form.get("scooter_id")
    repair_id = request.form.get("repair_id")
    data = {"name": "repair-fixed", "scooter_id": scooter_id, "repair_id": repair_id}
    response = get_connection().send(data)
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return redirect(url_for("engineer.update_report"))
