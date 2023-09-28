"""
Engineer Blueprint

This module defines the routes and views related to the engineer's functionality in the application.

"""
from flask import Blueprint, render_template
# from agent_common import comms

engineer = Blueprint("engineer", __name__)

@engineer.route("/engineer/scooters/locations")
def scooter_locations():
    """
    Display the locations of reported scooters page.

    Returns:
        Flask response: The reported scooters location page with Google Maps displayed.
    """
    return render_template("engineer/pages/locations.html")
