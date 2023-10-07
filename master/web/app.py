"""
Master Application

This module provides a function to create and configure the Flask application for the master pi.
It initializes the database and registers blueprints for the admin site and database API.

"""
from flask import Flask
from master.database.database_manager import init_db
from master.database.seed import seed_data
from master.web.admin_site import admin
from master.web.database.faces import face_api
from master.web.database.users import users_api
from master.web.database.scooters import scooter_api
from master.web.database.bookings import booking_api
from master.web.database.repairs import repairs_api
from master.web.database.transactions import transaction_api
from master.web.mail import init_mail

def create_master_app(testing=False):
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    
    app.secret_key = 'abc123'
    
    init_db(app, testing)
    init_mail(app)
   
    with app.app_context():
        if not testing:
            seed_data()
   
    blueprints = [
        admin,
        users_api,
        face_api,
        scooter_api,
        booking_api,
        repairs_api,
        transaction_api,
    ]
  
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
  
    return app
