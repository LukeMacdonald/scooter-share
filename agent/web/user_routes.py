"""
User Routes Blueprint

This blueprint defines routes related to user management, including login, signup,
and role-based redirections to customer and engineer home pages.

"""
from flask import Blueprint, render_template, request, redirect, url_for
from agent_common import comms

user = Blueprint("user", __name__)

# Connect the first time that we use a connection.
conn = None
def get_connection() -> comms.Connection:
    global conn
    if conn is None:
        conn = comms.Connection('0.0.0.0', 12345)
    return conn

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
    email = request.form.get('email')
    password = request.form.get('password')

    data = {
        "email": email,
        "password": password,
        "name": "login"
    }
    
    # role = "customer"
    
    # if role == "customer":
    #     return redirect(url_for('user.customer_home'))
    # elif role == "engineer":
    #     return redirect(url_for('user.engineer_home'))
    # else:
    #     # todo: Add error response
    #     pass
    
    # communicate with the master
    response = get_connection().send(data)
    print(response)

    # if receives confirmation and user type from master
    if response["response"] == "yes":
        if response["role"] == "customer":
            return redirect(url_for('user.customer_home'))
        elif response["role"] == "engineer":
            return redirect(url_for('user.engineer_home'))
@user.route("/signup")
def signup():
    """
    Display the login page.

    Returns:
        Flask response: The login page.
    """
    return render_template("register.html")

@user.route("/signup", methods=["POST"])
def signup_post():
    """
    Handle the signup form submission.

    Extracts user data from the form and performs the signup process.
    """
    data = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'role': request.form.get('role'),
            "name": "register"
    }
    response = get_connection().send(data)

    print(response)

    if response["response"] == "yes":
        if response["role"] == "customer":
            return redirect(url_for('user.customer_home'))
        elif response["role"] == "engineer":
            return redirect(url_for('user.engineer_home'))

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
