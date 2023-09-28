from flask import Flask
from master.web.admin_site import admin
from master.web.database.database_manager import init_db
from master.web.database.api import db_api


def create_master_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)    
    init_db(app)
    app.register_blueprint(admin)
    app.register_blueprint(db_api)
    return app