"""
Blueprint for Admin Routes

"""
from datetime import datetime
from passlib.hash import sha256_crypt
from requests.exceptions import RequestException
from flask import Blueprint, render_template, redirect, url_for, request
from master.agent_interface import helpers
from master.web.mail import send_email
from master.database.models import User, RepairStatus, UserType
import master.web.database.bookings as bookings_api
import master.web.database.repairs as repairs_api
import master.web.database.scooters as scooters_api
import master.web.database.users as user_api

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
            return redirect(url_for('admin.home'))
    return redirect("/")

@admin.route("/home")
def home():
    """
    Display the admin home page.

    Returns:
        Flask response: The admin home page.
    """
    scooters = scooters_api.get_all()
    bookings = bookings_api.get_all()
    customers = user_api.get_all_by_role(UserType.CUSTOMER.value)
    
    for scooter in scooters:
        scooter['location'] = helpers.get_street_address(scooter["latitude"], scooter["longitude"])
    for booking in bookings:
        start_time = datetime.strptime(booking["start_time"], "%a %d %b, %H:%M, %Y")
        end_time = datetime.strptime(booking["end_time"], "%a %d %b, %H:%M, %Y")
        time_difference = (end_time - start_time).total_seconds()/60
        booking['duration'] = str(time_difference)
    
    return render_template("admin/pages/home.html", scooters=scooters, bookings=bookings, customers=customers)

@admin.route("/scooter/bookings")
def bookings():
    """
    Display the admin page for scooter bookings.

    Returns:
        Flask response: The scooter bookings page.
    """
    return render_template("admin/pages/bookings.html")

@admin.route("/scooters/manage")
def manage_scooters():
    """
    Display the admin page for managing scooters.

    Returns:
        Flask response: The scooter management page.
    """
    return render_template("admin/pages/home.html")

@admin.route("/scooters/usage")
def scooter_usage():
    """
    Display the admin page for scooter usage statistics.

    Returns:
        Flask response: The scooter usage statistics page.
    """
    return render_template("admin/pages/home.html")

@admin.route("/customers/manage")
def manage_customers():
    """
    Display the admin page for managing customers.

    Returns:
        Flask response: The customer management page.
    """
    return render_template("admin/pages/home.html")
@admin.route("/customers/edit/<int:user_id>")
def edit_customer(user_id):
    customer = user_api.get(user_id)
    print(customer)
    
    return render_template("admin/pages/edit_user.html", data=customer)

@admin.route("/customer/update", methods=['POST'])
def update_customer():
    try:
        user_id = request.form.get('user_id')
        user = user_api.get(user_id)
        user["first_name"] = request.form.get('first_name')
        user["last_name"] = request.form.get('last_name')  
        user["phone_number"] = request.form.get('phone_number')
        user_api.update(user_id, user)
        return redirect(url_for("admin.home")) 
    except Exception as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500  
@admin.route("/scooter/add")
def add_scooter():
    return render_template("admin/pages/add_scooter.html")

@admin.route("/scooter/submit", methods=['POST'])
def submit_scooter():
    data = {
        "make": request.form.get('make'),
        "cost_per_time": request.form.get('cost'),
        "colour": request.form.get('colour'),
        "latitude": request.form.get('latitude'),
        "longitude": request.form.get('longitude')
    }
    scooters_api.post(data)
    return redirect(url_for("admin.home")) 
@admin.route("/customers/info")
def customers_info():
    """
    Display the admin page for customer information.

    Returns:
        Flask response: The customer information page.
    """
    return render_template("admin/pages/home.html")

@admin.route("/admin/repairs")
def confirm_reports():
    """
    Endpoint to retrieve and display pending repair reports for admin confirmation.

    Returns:
        str: Rendered HTML template containing pending repair reports.
    """
    try:
        repairs = repairs_api.get_pending_repairs()
        return render_template("admin/pages/scooter_repairs.html", repairs_data=repairs)
    except Exception as error:
        print(f"Error during repairs API request: {error}")
        return {"error": "Internal Server Error"}, 500
   
@admin.route("/admin/scooter/report", methods=['POST'])
def report_scooter():
    """
    Endpoint to process scooter repair reports submitted by users.

    Returns:
        Response: Redirects admin to the confirm_reports endpoint after processing the report.
    """
    try:
        repair_id = request.form.get('repair_id')
        
        updated_repair = repairs_api.update_status(repair_id, RepairStatus.ACTIVE.value)     
        
        # Send notifications to engineers
        notify_engineers(updated_repair["scooter_id"],updated_repair["report"])
    
        return redirect(url_for("admin.confirm_reports"))
    
    except RequestException as error:
        print(f"Error during API request: {error}")
        return {"error": "Internal Server Error"}, 500  
    
@admin.route("/admin/notify/<int:scooter_id>/<string:report>", methods=["GET"])
def notify_engineers(scooter_id, report):
    """
    Notifies engineers about a reported scooter repair request via email.
    """
    try: 
        
        scooter = scooters_api.get(scooter_id)
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
