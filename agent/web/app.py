"""
Agent Application Module

This module provides functions to create and configure a Flask application
for the agent, including the registration of user routes.

"""
from flask import Flask
from agent.web.user_routes import user
from agent.web.engineer_routes import engineer
from database.models import User
from flask_login import LoginManager

def create_agent_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Initialize and configure Flask-Login
    # login_manager = LoginManager()
    # login_manager.login_view = "user.login"
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    # Register your blueprints
    app.register_blueprint(user)
    app.register_blueprint(engineer)
    
    # Set the secret key
    app.secret_key = 'secret_key'

    return app

