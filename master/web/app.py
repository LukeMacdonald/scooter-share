from flask import Flask
from flask_site import site
from database.database_manager import init_db
from database.api import db_api
import os


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    # basedir = os.path.abspath(os.path.dirname(__file__))
    
    init_db(app)
    
    app.register_blueprint(site)
    app.register_blueprint(db_api)
    
    return app


if __name__ == '__main__':
    flask_app = create_app() 
    
    # Only allow access from the specific host (replace '127.0.0.1' with your desired host)
    flask_app.run(host='127.0.0.1', port=5000, debug=True)