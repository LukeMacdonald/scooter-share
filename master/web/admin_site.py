from flask import Flask, Blueprint, render_template, session,request, redirect, url_for

admin = Blueprint("admin", __name__)

# Client webpage.
@admin.route("/admin")
def index():
    return render_template("login.html")

@admin.route("/admin/login", methods=['POST'])
def login():
    print(request.form.get('email'))
    # Perform login logic
    return redirect(url_for('admin.home'))
    
@admin.route("/admin/home")
def home():
    return render_template("admin/home.html")

@admin.route("/admin/home/calendar")
def calendar():
    return render_template("admin/calender.html")

@admin.route("/admin/home/maps")
def maps():
    return render_template("admin/maps.html")