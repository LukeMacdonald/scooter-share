"""
Database Configuration and Initialization

This module contains code for configuring and initializing the Flask-SQLAlchemy extension.
It establishes a connection to the MySQL database and creates the necessary database tables.

"""
from flask_sqlalchemy import SQLAlchemy
from master.database.config import HOST, USER, PASSWORD, NAME


db = SQLAlchemy()

def init_db(app):
    """
    Initialize the SQLAlchemy extension and configure it with the provided Flask app.

    Args:
        app (Flask): The Flask application instance to which SQLAlchemy should be initialized.
        
    Returns:
        None
    """
    # Load configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{USER}:{PASSWORD}@{HOST}/{NAME}""
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

    # Initialize SQLAlchemy extension
    db.init_app(app)
     # Create all database tables
    with app.app_context():
        db.create_all()
