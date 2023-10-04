"""
Blueprint for Admin Routes

"""
from constants import API_BASE_URL
from flask import Blueprint, render_template, redirect, url_for, request
from master.agent_interface import helpers
from master.database.database_manager import db
from master.database.models import Repairs, RepairStatus
from master.database.models import User, UserType, Scooter, Booking, ScooterStatus, BookingState, RepairStatus, Repairs, Transaction
from master.web.mail import send_email
from passlib.hash import sha256_crypt

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
    scooters = Scooter.query.all()
    bookings = Booking.query.all()
    customers = User.query.filter_by(role="customer")
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
    repairs = [repair.as_json()
               for repair in Repairs.query.filter_by(status=RepairStatus.PENDING.value).all()]
    return render_template("admin/pages/scooter_repairs.html", repairs_data=repairs)
   
@admin.route("/admin/scooter/report", methods=['POST'])
def report_scooter():
    repair_id = request.form.get('repair_id')
    repair = Repairs.query.get(int(repair_id))
    repair.status = RepairStatus.ACTIVE.value
    db.session.commit()
    notify_engineers(repair["scooter_id"], repair["report"])
    return redirect(url_for("admin.confirm_reports"))
    
@admin.route("/admin/notify/<int:scooter_id>/<string:report>", methods=["GET"])
def notify_engineers(scooter_id, report):
    """
    Notifies engineers about a reported scooter repair request via email.
    """
    try:
        scooter = Scooter.get(int(scooter_id))
        latitude = scooter.latitude
        longitude = scooter.longitude
        steet_address = helpers.get_street_address(latitude, longitude)
        # Currently only setting engineer email to personal account to prevent sending randoms people emails
        # engineer_emails = requests.get(f"{API_BASE_URL}/engineer_emails", timeout=5).json()
        engineer_emails = ["lukemacdonald560@gmail.com","lukemacdonald21@gmail.com"]
        email_subject = 'URGENT: Scooter Repair Request'
        email_body = helpers.get_email_body(scooter_id, report, steet_address, email_subject)
        # Send the email
        send_email(email_subject, engineer_emails, email_body)
        return "Email sent successfully!", 200
    except Exception as error:
        print(str(error))
        return "Email sending failed", 500   
