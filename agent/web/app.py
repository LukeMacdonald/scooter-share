from flask import Flask
from agent.web.user_routes import user
from agent_common import comms

def create_agent_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.register_blueprint(user)
    return app