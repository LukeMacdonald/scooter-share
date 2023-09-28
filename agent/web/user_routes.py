from flask import Blueprint, render_template, request, redirect, url_for
from agent_common import comms

user = Blueprint("user", __name__)

# connection = comms.Connection()

@user.route("/")
def login():
    """
    Display the login page.

    Returns:
        Flask response: The login page.
    """
    return render_template("login.html")

@user.route("/login", methods=["POST"])
def login_post():
    """
    Handle the login form submission.

    Redirects the user based on their role (customer or engineer).
    """
    username = request.form.get('username')
    password = request.form.get('password')

    data = {
        "username": username,
        "password": password,
        "name": "login"
    }
    
    role = "engineer"
    
    if role == "customer":
        return redirect(url_for('user.customer_home'))
    elif role == "engineer":
        return redirect(url_for('user.engineer_home'))
    else:
        # todo: Add error response
        pass
    
    # # communicate with the master
    # response = connection.send(data)
    # # if receives confirmation and user type from master
    # if response["name"] == "yes":
    #     if response["user_type"] == "customer":
    #         redirect(url_for('user_homepage'))
    #     elif response["engineer_type"] == "engineer":
    #         redirect(url_for('engineer_homepage'))

@user.route("/signup", methods=["POST"])
def signup():
    """
    Handle the signup form submission.

    Extracts user data from the form and performs the signup process.
    """
    data = {
            #Auto assign an id?
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name')
    }

@user.route("/customer")
def customer_home():
    """
    Display the customer home page.

    Returns:
        Flask response: The customer home page.
    """
    return render_template("customer/pages/home.html")

@user.route("/engineer")
def engineer_home():
    """
    Display the engineer home page.

    Returns:
        Flask response: The engineer home page.
    """
    return render_template("engineer/pages/home.html")
