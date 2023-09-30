"""
Agent Application Module

This module provides functions to create and configure a Flask application
for the agent, including the registration of user routes.

"""
from flask import Flask
from agent.web.user_routes import user
from agent.web.engineer_routes import engineer

def create_agent_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(engineer)
    app.secret_key = 'secret_key'
    return app
