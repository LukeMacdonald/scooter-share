from flask import Flask, Blueprint, render_template

admin = Blueprint("admin", __name__)

# Client webpage.
@admin.route("/admin/login")
def index():
    return render_template("admin_login.html")
