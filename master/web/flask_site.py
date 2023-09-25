from flask import Flask, Blueprint, render_template

site = Blueprint("site", __name__)

# Client webpage.
@site.route("/")
def index():
    return render_template("index.html")
