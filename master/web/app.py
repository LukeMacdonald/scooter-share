"""
Master Application

This module provides a function to create and configure the Flask application for the master pi.
It initializes the database and registers blueprints for the admin site and database API.

"""
from flask import Flask
from master.web.admin_site import admin
from database.database_manager import init_db
from database.api.users import users_api
from database.api.scooters import scooter_api
from database.api.bookings import booking_api
from database.api.repairs import repairs_api
from database.api.transactions import transaction_api
from database.seed import seed_data


def create_master_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
   
    init_db(app)
   
    with app.app_context():
        seed_data()
   
    blueprints = [
        admin,
        users_api,
        scooter_api,
        booking_api,
        repairs_api,
        transaction_api,
    ]
  
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
  
    return app
