"""
User Routes Blueprint

This blueprint defines routes related to user management, including login, signup,
and role-based redirections to customer and engineer home pages.

"""
from agent.common import comms, socket_utils
from agent.web.connection import get_connection
from agent.web.google_api import calendar
from datetime import datetime, date, timedelta
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from agent.web.login import user_login_req
import os

cal = None

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
    if "user" in response:
        global cal
        cal = calendar.GoogleCalendar()
        if response["user"]["role"] == "customer":
            session['user_info'] = response["user"]
            return redirect(url_for('user.customer_home'))
        elif response["user"]["role"] == "engineer":
            session['eng_info'] = response["user"]
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
    if "user" in response:
        global cal
        cal = calendar.GoogleCalendar()
        if response["user"]["role"] == "customer":
            session["user_info"] = response["user"]
            return redirect(url_for('user.customer_home'))
        elif response["user"] == "engineer":
            session['eng_info'] = response["user"]
            return redirect(url_for('engineer.home'))
        else:
            raise ValueError("wat")
    else:
        return redirect("/signup")

@user.route("/customer")
@user_login_req
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
    return render_template("customer/pages/home.html",
                           scooters=response["scooters"],
                           customer=response["user_details"],
                           bookings=response["bookings"])

@user.route('/make_booking/<int:scooter_id>/<float:balance>/<float:cost_per_time>')
@user_login_req
def make_booking(scooter_id, balance, cost_per_time):
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: The make-booking page.
    """
    return render_template("customer/pages/make-booking.html", scooter_id=scooter_id, balance=balance, cost_per_time=cost_per_time)

@user.route('/make_booking/<int:scooter_id>', methods=["POST"])
@user_login_req
def make_booking_post(scooter_id):
    """
    Display the page for booking a scooter.

    Returns:
        Flask response: post request for make-booking, returns homepage.
    """

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

    calendar_info = {
        "time_start" : start_datetime,
        "time_end": end_datetime,
        "description": f"{duration} {request.form.get('duration-unit')} booking of Scooter {scooter_id}.",
        "summary": f"Scooter {scooter_id} booking!"
    }

    event_id = cal.insert(calendar_info)

    data = {
        "data": {
        "scooter_id": scooter_id,
        "user_id": customer_info["id"],
        "date": date.today().isoformat(),
        "start_time": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "event_id": event_id
        },
        "name": "make-booking"
    }

    get_connection().send(data)


    return redirect(url_for('user.customer_home'))

@user.route('/cancel-booking', methods=["POST"])
@user_login_req
def cancel_booking():
    """
    Cancel a booking.

    Sends a request to cancel a booking to the server, removes the associated
    calendar event, and redirects the user to the customer home page.

    Returns:
        Flask response: A redirect response to the customer home page.
    """
    get_connection().send({"name" : "cancel-booking", "booking-id" : request.form.get("booking_id")})

    calendar.remove(request.form.get("event_id"))

    return redirect(url_for('user.customer_home'))

@user.route('/report-issue/<int:scooter_id>', methods=["POST"])
def report_issue(scooter_id):
    """
    Report an issue with a scooter.

    Sends a report issue request to the server for a specific scooter and redirects
    the user to the customer home page.

    Args:
        scooter_id (int): The ID of the scooter for which the issue is being reported.

    Returns:
        Flask response: A redirect response to the customer home page.
    """
    response = get_connection().send({"name" : "report-issue", "scooter-id" : scooter_id, "report": request.form.get("issue_description")})

    return redirect(url_for('user.customer_home'))

@user.route('/top-up-balance')
@user_login_req
def top_up_balance():
    """
    Display the page for topping up balance.

    Returns:
        Flask response: The top-up-balance page.
    """
    return render_template("customer/pages/top-up-balance.html")

@user.route('/top-up-balance', methods=["POST"])
@user_login_req
def top_up_balance_post():
    """
    Display the page for topping up balance.

    Returns:
        Flask response: The top-up-balance page.
    """
    get_connection().send({"user-id": session.get('user_info')['id'], 
                                      "amount": request.form.get("amount"), "name": "top-up-balance"})

    return redirect(url_for('user.customer_home'))

@user.route('/logout')
def logout():
    """
    Log out the user.

    Clears the current user's session, deletes a specific local file (if it exists),
    and redirects the user to the login page.

    Returns:
        Flask response: A redirect response to the login page.
    """
    session.clear()

    file_path = "token.json"

    try:
        os.remove(file_path)
        print(f"File {file_path} has been successfully deleted.")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
    return redirect(url_for('user.login'))