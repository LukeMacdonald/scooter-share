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
        Flask response: The engineer home page or an error page.
    """

    data = {"name": "locations"}
    response = get_connection().send(data)
    
    if "error" in response:
        error_message = 'Internal Server Error! Please Login Again!'
        return redirect(url_for('user.logout', error_message=error_message))

    return render_template("engineer/pages/home.html", scooter_data=response["data"])

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
        if response["error"] == "Unauthorised":
            return redirect(url_for('user.logout' ))
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return redirect(url_for("engineer.home"))
