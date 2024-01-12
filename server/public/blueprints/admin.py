from datetime import datetime, date, timedelta
from flask import Blueprint,request, jsonify
from connection import get_connection

admin = Blueprint("admin", __name__)