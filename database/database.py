from config import HOST, USER, PASSWORD, NAME
from flask_sqlalchemy import SQLAlchemy

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
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{USER}:{PASSWORD}@{HOST}/{NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking

    # Initialize SQLAlchemy extension
    db.init_app(app)
    
     # Create all database tables
    with app.app_context():
        db.create_all()