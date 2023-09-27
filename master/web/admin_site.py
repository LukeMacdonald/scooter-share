"""
Blueprint for Admin Routes

Routes:
    - `/`: Display the login page for admin.
    - `/admin/login` (POST): Handle the admin login form submission.
    - `/home`: Display the admin home page.
    - `/scooter/bookings`: Display the admin page for scooter bookings.
    - `/scooters/manage`: Display the admin page for managing scooters.
    - `/scooters/usage`: Display the admin page for scooter usage statistics.
    - `/customers/manage`: Display the admin page for managing customers.
    - `/customers/info`: Display the admin page for customer information.
"""
from flask import Blueprint, render_template, redirect, url_for

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
    # Perform login logic here
    return redirect(url_for('admin.home'))

@admin.route("/home")
def home():
    """
    Display the admin home page.

    Returns:
        Flask response: The admin home page.
    """
    return render_template("admin/pages/home.html")

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
