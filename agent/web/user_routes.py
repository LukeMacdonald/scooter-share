"""
User Routes Blueprint

This blueprint defines routes related to user management, including login, signup,
and role-based redirections to customer and engineer home pages.

"""
from agent.common import comms, socket_utils
from agent.web.connection import get_connection
from datetime import datetime, date, timedelta
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session

user = Blueprint("user", __name__)

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
        
    # communicate with the master
    response = get_connection().send(data)
    print(response)

    if "user" in response:
        session['user_info'] = response["user"]
        if response["user"]["role"] == "customer":
            return redirect(url_for('user.customer_home'))
        elif response["user"]["role"] == "engineer":
            return redirect(url_for('engineer.home'))
    else:
        return redirect("/")
        

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
    if response["response"] == "yes":
        session["user_info"] = response["user"]
        if response["user"]["role"] == "customer":
            return redirect(url_for('user.customer_home'))
        elif response["user"] == "engineer":
            return redirect(url_for('engineer.home'))

@user.route("/customer")
def customer_home():
    """
    Display the customer home page.

    Returns:
        Flask response: The customer home page.
    """
    customer_info = session.get('user_info')
    data = {
        "customer_id": customer_info["id"],
        "name": "customer-homepage"
    }

    response = get_connection().send(data)
    print(response)

    return render_template("customer/pages/home.html",
                           scooters=response["scooters"],
                           customer=customer_info,
                           bookings=response["bookings"])

@user.route('/make_booking/<int:scooter_id>/<float:balance>/<float:cost_per_time>')
def make_booking(scooter_id, balance, cost_per_time):
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: The make-booking page.
    """
    return render_template("customer/pages/make-booking.html", scooter_id=scooter_id, balance=balance, cost_per_time=cost_per_time)

@user.route('/make_booking/<int:scooter_id>', methods=["POST"])
def make_booking_post(scooter_id):
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: The make-booking page.
    """

    ## TODO: calculate cost per time

    # add new booking to the database
    customer_info = session.get('user_info')

    start_time = request.form.get('start-time')
    duration = int(request.form.get('duration'))
    
    # Combine the start time with today's date to create a datetime object
    start_datetime = datetime.combine(date.today(), datetime.strptime(start_time, "%H:%M").time())
    if request.form.get('duration-unit') == "minutes":
        end_datetime = start_datetime + timedelta(minutes=duration)
    else:
        end_datetime = start_datetime + timedelta(hours=duration)

    data = {
        "data": {
        "scooter_id": scooter_id,
        "user_id": customer_info["id"],
        "date": date.today().isoformat(),
        "start_time": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active"
        },
        "name": "make-booking"
    }

    get_connection().send(data)

    calendar_info = {
        "time_start" : start_datetime,
        "time_end": end_datetime,
        "description": f"{duration} {request.form.get('duration-unit')} booking of Scooter {scooter_id}.",
        "summary": f"Scooter {scooter_id} booking!"
    }

    calendar.insert(calendar_info)

    return redirect(url_for('user.customer_home'))
