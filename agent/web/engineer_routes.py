"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
import logging
from flask import Blueprint, render_template, url_for, redirect, request
from agent.web.connection import get_connection

engineer = Blueprint("engineer", __name__)

logging.basicConfig(level=logging.ERROR)

@engineer.route("/engineer")
def home():
    """
    Display the engineer home page.

    Returns:
        Flask response: The engineer home page.
    """
    try:
        data = {"name": "locations"}
        response = get_connection().send(data) 
        if "status_code" in response and response["status_code"] == 200:
            return render_template("engineer/pages/home.html", scooter_data=response["data"])
        else:
            error_message = response.get("error", "Unknown error occurred.")
            return render_template("engineer/pages/error.html", error=error_message), 500
    except Exception as error:
        # Log the exception for debugging purposes
        logging.error("Error occurred: %s", error)
        # Render an error template with a user-friendly message
        return render_template("error.html", error="An unexpected error occurred."), 500

@engineer.route("/engineer/scooters/locations")
def scooter_locations():
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """
    try:
        data = {"name": "locations"}
        response = get_connection().send(data)
        print(response)
        
        if "status_code" in response and response["status_code"] == 200:
            return render_template("engineer/pages/locations.html", scooter_data=response["data"])
        else:
            error_message = response.get("error", "Unknown error occurred.")
            return render_template("engineer/pages/error.html", error=error_message), 500

    except Exception as error:
        # Log the exception for debugging purposes
        logging.error("Error occurred: %s", error)
        # Render an error template with a user-friendly message
        return render_template("error.html", error="An unexpected error occurred."), 500

@engineer.route("/engineer/scooters/repairs")
def update_repair_report():
    """
    Display the update repair report page for engineers.

    Returns:
        Flask response: The update repair report page.
    """
    try:
        data = {"name": "locations"}
        response = get_connection().send(data)
        if "status_code" in response and response["status_code"] == 200:
            return render_template("engineer/pages/update_repair.html", scooter_data=response["data"])
        else:
            error_message = response.get("error", "Unknown error occurred.")
            return render_template("engineer/pages/error.html", error=error_message), 500

    except Exception as error:
        # Log the exception for debugging purposes
        logging.error("Error occurred: %s", error)
        # Render an error template with a user-friendly message
        return render_template("error.html", error="An unexpected error occurred."), 500

@engineer.route("/engineer/scooter/fixed", methods=["POST"])
def scooter_fixed():
    """
    Handle the scooter fixed form submission for engineers.

    Returns:
        Flask redirect: Redirects back to the update repair report page.
    """
    try:
        scooter_id = request.form.get("scooter_id")
        repair_id = request.form.get("repair_id")
        data = {"name": "repair-fixed", "scooter_id": scooter_id, "repair_id": repair_id}
        response = get_connection().send(data)
        print(response)
        if "status_code" in response and response["status_code"] == 200:
            return redirect(url_for("engineer.update_repair_report"))
        else:
            error_message = response.get("error", "Unknown error occurred.")
            return render_template("engineer/pages/error.html", error=error_message), 500

    except Exception as error:
        # Log the exception for debugging purposes
        logging.error("Error occurred: %s", error)
        # Render an error template with a user-friendly message
        return render_template("error.html", error="An unexpected error occurred."), 500
