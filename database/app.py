from flask import Flask
from database import init_db
from api.user import user_api

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Initialize SQLAlchemy extension
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(user_api)

    return app

if __name__ == "__main__":
    flask_app = create_app()  # Rename the variable to avoid conflict
    flask_app.run(host="0.0.0.0", port=5000)