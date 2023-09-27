from flask import Flask
from user_routes import user
import sys
import os


# Get the path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
# Now you can import the module
from agent_common import comms
# Restoring sys.path to its original state (optional)
sys.path.remove(parent_dir)

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.register_blueprint(user)
    return app

if __name__ == '__main__':
    flask_app = create_app()
    
    # Only allow access from the specific host (replace '127.0.0.1' with your desired host)
    flask_app.run(host='0.0.0.0', port=5000, debug=True)

    connection = comms.Connection()
