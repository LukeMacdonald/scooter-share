from flask import Blueprint, render_template, request, redirect, url_for

admin = Blueprint("admin", __name__)

# Client webpage.
@admin.route("/")
def index():
    return render_template("login.html")

@admin.route("/admin/login", methods=['POST'])
def login(): 
    # Perform login logic
    return redirect(url_for('admin.home'))
    
@admin.route("/home")
def home():
    return render_template("admin/pages/home.html")

@admin.route("/scooter/bookings")
def bookings():
    return render_template("admin/pages/bookings.html")

@admin.route("/scooters/manage")
def manage_scooters():
    return render_template("admin/pages/home.html")

@admin.route("/scooters/usage")
def scooter_usage():
    return render_template("admin/pages/home.html")

@admin.route("/customers/manage")
def manage_customers():
    return render_template("admin/pages/home.html")
@admin.route("/customers/info")
def customers_info():
   return render_template("admin/pages/home.html") 