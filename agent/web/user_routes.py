"""
User Routes Blueprint

This blueprint defines routes related to user management, including login, signup,
and role-based redirections to customer and engineer home pages.

"""

from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from agent.web.login import user_login_req
from agent.web.connection import get_connection
from agent.web.google_api import calendar

calendar = calendar.GoogleCalendar()
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
        if response["user"]["role"] == "customer":
            session['user_info'] = response["user"]
            return redirect(url_for('user.customer_home'))
        elif response["user"]["role"] == "engineer":
            session['eng_info'] = response["user"]
            return redirect(url_for('engineer.home'))
        else:
            error_message= "Admin can only sign in on the master pi"
            flash(error_message, category='login_error')  # Flash the error message
            return redirect(url_for('user.login'))
    else:
        error_message = response.get("error", "Login failed. Please try again.")
        flash(error_message, category='login_error')  # Flash the error message
        return redirect(url_for('user.login'))
        

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
            'phone_number': request.form.get('phone_number'),
            "name": "register"
    }

    response = get_connection().send(data)
    if "user" in response:
        session["user_info"] = response["user"]
        if response["user"]["role"] == "customer":
            return redirect(url_for('user.customer_home'))
        elif response["user"] == "engineer":
            return redirect(url_for('engineer.home'))
        else:
            error_message = "Invalid role!"
            flash(error_message, category='signup_error')  # Flash the error message
            return redirect(url_for('user.signup'))
    else:
        error_message = response.get("error", "Signup failed. Please try again.")
        flash(error_message, category='signup_error')  # Flash the error message
        return redirect(url_for('user.signup'))

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
        Flask response: The make-booking page.
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

    event_id = calendar.insert(calendar_info)

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

    response = get_connection().send(data)
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return redirect(url_for('user.customer_home'))

@user.route('/cancel-booking', methods=["POST"])
@user_login_req
def cancel_booking():
    response = get_connection().send({"name" : "cancel-booking", "booking-id" : request.form.get("booking_id")})
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        calendar.remove(request.form.get("event_id"))
        return redirect(url_for('user.customer_home'))

@user.route('/report-issue/<int:scooter_id>', methods=["POST"])
def report_issue(scooter_id):
    
    response = get_connection().send({"name" : "report-issue", "scooter-id" : scooter_id, "report": request.form.get("issue_description")})
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else: 
        return redirect(url_for('user.customer_home'))

@user.route('/unlock')
@user_login_req
def scan_to_unlock():
    return render_template("customer/pages/scan.html", title="Scan to unlock scooter", then="unlock")

@user.route('/unlock/<int:id>')
@user_login_req
def unlock_scooter(id):
    response = get_connection().send({"name": "unlock-scooter", "scooter_id": id, "user_id": session["user_info"]["id"]})
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else: 
        return redirect(url_for('user.customer_home'))

@user.route('/return')
@user_login_req
def scan_to_return():
    return render_template("customer/pages/scan.html", title="Scan to return scooter", then="return")

@user.route('/return/<int:id>')
@user_login_req
def return_scooter(id):
    response = get_connection().send({"name": "lock-scooter", "scooter_id": id, "user_id": session["user_info"]["id"]})
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else: 
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
    response = get_connection().send({"user-id": session.get('user_info')['id'], 
                                      "amount": request.form.get("amount"), "name": "top-up-balance"})
    if "error" in response:
        return redirect(url_for('user.error',message=response['error'] ))
    else:
        return redirect(url_for('user.customer_home'))

@user.route('/error', defaults={'message': 'An error occurred.'})
@user.route('/error/<string:message>')
def error(message):
    return render_template('error.html', message=message, role=session['user_info']["role"])

@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))
