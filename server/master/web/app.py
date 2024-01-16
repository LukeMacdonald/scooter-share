"""
Master Application

This module provides a function to create and configure the Flask application for the master pi.
It initializes the database and registers blueprints for the admin site and database API.

"""
from flask import Flask
from flask_cors import CORS
from database.database_manager import init_db
from database.seed import seed_data
from web.admin_site import admin
from web.database.faces import face_api
from web.database.users import users_api
from web.database.scooters import scooter_api
from web.database.bookings import booking_api
from web.database.repairs import repairs_api
from web.database.transactions import transaction_api
from web.mail import init_mail

def create_master_app(testing=False):
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    
    CORS(app)
    
    app.secret_key = 'abc123'
    
    init_db(app, testing)
    init_mail(app)
   
    with app.app_context():
        if not testing:
            seed_data()
   
    blueprints = [
        users_api,
        face_api,
        scooter_api,
        booking_api,
        repairs_api,
        transaction_api,
    ]
  
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
    app.register_blueprint(admin, url_prefix='/admin')
  
    return app
