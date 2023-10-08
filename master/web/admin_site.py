"""
Blueprint for Admin Routes

"""
import requests
from passlib.hash import sha256_crypt
from requests.exceptions import RequestException
from flask import Blueprint, render_template, redirect, url_for, request, session
from master.agent_interface import helpers
from master.web.mail import send_email
from master.database.models import User, RepairStatus, UserType, BookingState
from master.web.login import admin_login_req

API_BASE_URL = "http://localhost:5000"

admin = Blueprint("admin", __name__)

@admin.route("/")
def index():
    """
    Display the login page for admin.

    Returns:
        Flask response: The login page.
    """
    return render_template("login.html")

@admin.route("/admin/login", methods=['POST'])
def login():
    """
    Handle the admin login form submission.

    Perform login logic and redirect to the admin home page.

    Returns:
        Flask response: Redirect to the admin home page.
    """
    admin = User.query.filter_by(role='admin', email=request.form.get("email")).first()

    if admin is not None:
        password = request.form.get("password")
        if sha256_crypt.verify(password, admin.password):
            session['admin_info'] = admin.email
            return redirect(url_for('admin.home'))
    return redirect("/")

@admin.route("/home")
@admin_login_req
def home():
    """
    Display the admin home page.

    Returns:
        Flask response: The admin home page.
    """
    scooters =  requests.get(f"{API_BASE_URL}/scooters/all", timeout=5).json() 
    customers = requests.get(f"{API_BASE_URL}/user/role/{UserType.CUSTOMER.value}", timeout=5).json() 
    
    for scooter in scooters:
        scooter['location'] = helpers.get_street_address(scooter["latitude"], scooter["longitude"])
 
    
    return render_template("admin/pages/home.html", scooters=scooters, customers=customers)

@admin.route("/scooter/bookings")
@admin_login_req
def bookings():
    """
    Display the admin page for scooter bookings.

    Returns:
        Flask response: The scooter bookings page.
    """
    bookings = requests.get(f"{API_BASE_URL}/bookings/status/{BookingState.COMPLETED.value}", timeout=5).json()
    
    for booking in bookings:
        booking["start_time"] = helpers.convert_time_format(booking["start_time"])
        
        
    return render_template("admin/pages/bookings.html", bookings=bookings)

@admin.route("/scooters/usage")
@admin_login_req
def scooter_usage():
    """
    Display the admin page for scooter usage statistics.

    Returns:
        Flask response: The scooter usage statistics page.
    """
    bookings = requests.get(f"{API_BASE_URL}/bookings/status/{BookingState.COMPLETED.value}", timeout=5).json()
    for booking in bookings:
        booking["duration"] = helpers.calculate_duration(booking["start_time"], booking["end_time"])
        booking["start_time"] = helpers.convert_time_format(booking["start_time"])
    return render_template("admin/pages/usage.html", bookings=bookings)

@admin.route("/customers/edit/<int:user_id>")
@admin_login_req
def edit_customer(user_id):
    """
    Edit customer information.

    Args:
        user_id (int): The unique identifier for the customer.

    Returns:
        str: Rendered template for editing user information.
    """
    response = requests.get(f"{API_BASE_URL}/user/id/{user_id}", timeout=5)   
    customer = response.json()

    return render_template("admin/pages/edit_user.html", data=customer)

@admin.route("/customer/update", methods=['POST'])
@admin_login_req
def update_customer():
    """
    Update customer information based on the form data.

    Returns:
        response: Redirect to the admin home page if successful, or error message with status code 500 if there is an error.
    """
    try:
        user_id = request.form.get('user_id')
        response = requests.get(f"{API_BASE_URL}/user/id/{user_id}", timeout=5)
        if response.status_code == 400:
            return {"error": "User Not Found"} 
        user = response.json()
            
        user["first_name"] = request.form.get('first_name')
        user["last_name"] = request.form.get('last_name')  
        user["phone_number"] = request.form.get('phone_number')
        updated_user = requests.put(f"{API_BASE_URL}/user/{user_id}", json=user, timeout=5).json()
        return redirect(url_for("admin.home")) 
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500

@admin.route("/customer/delete/<int:user_id>")
@admin_login_req
def delete_customer(user_id):
    """
    Delete a customer record.

    Args:
        user_id (int): The unique identifier for the customer.

    Returns:
        response: Redirect to the admin home page if successful, or error message with status code 500 if there is an error.
    """
    try:
        requests.delete(f"{API_BASE_URL}/user/{user_id}", timeout=5).json()
        return redirect(url_for("admin.home"))
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500   

@admin.route("/scooter/add")
@admin_login_req
def add_scooter():
    """
    Render the template for adding a new scooter.

    Returns:
        str: Rendered template for adding a new scooter.
    """
    return render_template("admin/pages/add_scooter.html")

@admin.route("/scooter/edit/<int:scooter_id>")
@admin_login_req
def edit_scooter(scooter_id):
    """
    Edit scooter information based on the provided scooter ID.

    Args:
        scooter_id (int): The unique identifier for the scooter to be edited.

    Returns:
        str: Rendered template for editing scooter information if successful.
             If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5)
        if response.status_code == 404:
            return {"error": "Scooter Not Found"}
        scooter = response.json()
        return render_template("admin/pages/edit_scooter.html", data=scooter)
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500 

@admin.route("/scooter/update", methods=['POST'])
@admin_login_req
def scooter_update():
    """
    Update scooter information based on the form data provided via a POST request.

    Returns:
        response: Redirect to the admin home page if the update is successful.
                 If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:
        scooter_id = request.form.get('scooter_id')
        response = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5)
        if response.status_code == 404:
            return {"error": "Scooter Not Found"}
       
        scooter = response.json()
        scooter["colour"] = request.form.get("colour")
        scooter["make"] = request.form.get('make')
        scooter["cost_per_time"] = float(request.form.get('cost'))
        scooter["remaining_power"] = float(request.form.get('charge'))
        scooter["longitude"] = float(request.form.get('longitude'))
        scooter["latitude"] = float(request.form.get('latitude'))
        
        updated_scooter = requests.put(f"{API_BASE_URL}/scooter/id/{scooter_id}", json=scooter, timeout=5).json() 
        return redirect(url_for("admin.home")) 
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500 
        
@admin.route("/scooter/delete/<int:scooter_id>")
@admin_login_req
def delete_scooter(scooter_id):
    """
    Delete a scooter record based on the provided scooter ID.

    Args:
        scooter_id (int): The unique identifier for the scooter to be deleted.

    Returns:
        response: Redirect to the admin home page if the deletion is successful.
                 If there is an error, returns a dictionary with an error message and status code 500.
    """
    try:
        requests.delete(f"{API_BASE_URL}/scooter/{scooter_id}", timeout=5).json() 
        #scooters_api.delete(scooter_id)
        return redirect(url_for("admin.home"))
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500  
      
@admin.route("/scooter/submit", methods=['POST'])
@admin_login_req
def submit_scooter():

    """
    Handle the submission of a new scooter based on the form data provided via a POST request.

    Returns:
        response: Redirect to the admin home page if the submission is successful.
    """
    data = {
        "make": request.form.get('make'),
        "cost_per_time": request.form.get('cost'),
        "colour": request.form.get('colour'),
        "latitude": request.form.get('latitude'),
        "longitude": request.form.get('longitude')
    }
    scooter = requests.post(f"{API_BASE_URL}/scooter", json=data, timeout=5).json() 
    return redirect(url_for("admin.home")) 

@admin.route("/admin/repairs")
@admin_login_req
def confirm_reports():
    """
    Endpoint to retrieve and display pending repair reports for admin confirmation.

    Returns:
        str: Rendered HTML template containing pending repair reports.
    """
    try:
        repairs = requests.get(f"{API_BASE_URL}/repairs/pending", timeout=5).json()  
        return render_template("admin/pages/repairs.html", repairs_data=repairs)
    except Exception as error:
        print(f"Error during repairs API request: {error}")
        return {"error": "Internal Server Error"}, 500
   
@admin.route("/admin/scooter/report", methods=['POST'])
@admin_login_req
def report_scooter():
    """
    Endpoint to process scooter repair reports submitted by users.

    Returns:
        Response: Redirects admin to the confirm_reports endpoint after processing the report.
    """
    try:
        repair_id = request.form.get('repair_id')
        data = {"status": RepairStatus.ACTIVE.value}
        updated_repair = requests.put(f"{API_BASE_URL}/repair/status/{repair_id}", json=data, timeout=5).json()      
        # Send notifications to engineers
        notify_engineers(updated_repair["scooter_id"],updated_repair["report"])
    
        return redirect(url_for("admin.confirm_reports"))
    
    except RequestException as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500  
    
@admin.route("/admin/notify/<int:scooter_id>/<string:report>", methods=["GET"])
@admin_login_req
def notify_engineers(scooter_id, report):
    """
    Notifies engineers about a reported scooter repair request via email.
    """
    try: 
        
        scooter = requests.get(f"{API_BASE_URL}/scooter/id/{scooter_id}", timeout=5).json() 
        steet_address = helpers.get_street_address(scooter["latitude"], scooter["longitude"])
        # Currently only setting engineer email to personal account to prevent sending randoms people emails
        # engineer_emails = user_api.get_engineer_emails()
        engineer_emails = ["lukemacdonald560@gmail.com","lukemacdonald21@gmail.com"]
        email_subject = 'URGENT: Scooter Repair Request'
        email_body = helpers.get_email_body(scooter_id, report, steet_address, email_subject)
        # Send the email
        send_email(email_subject, engineer_emails, email_body)
        return "Email sent successfully!", 200
    except Exception as error:
        print(str(error))
        return "Email sending failed", 500 

@admin.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.index'))