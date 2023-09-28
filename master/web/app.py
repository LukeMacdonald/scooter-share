"""
Master Application

This module provides a function to create and configure the Flask application for the master pi.
It initializes the database and registers blueprints for the admin site and database API.

"""
from flask import Flask
from master.web.admin_site import admin
from master.web.database.database_manager import init_db
from master.web.database.api.users import users_api
from master.web.database.api.scooters import scooter_api
from master.web.database.seed import seedData



def create_master_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)    
    init_db(app)
    with app.app_context():
        seedData()
    app.register_blueprint(admin)
    app.register_blueprint(users_api)
    app.register_blueprint(scooter_api)
    return app