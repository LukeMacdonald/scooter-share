from flask import Blueprint, request, jsonify
from master.web.database.models import Booking
from master.web.database.database_manager import db

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    result = [
        {
            "BookingID": booking.BookingID,
            "UserID": booking.UserID,
            "ScooterID": booking.ScooterID,
            "Time": booking.Time.strftime("%Y-%m-%d %H:%M:%S"),
            "Status": booking.Status
        }
        for booking in bookings
    ]
    return jsonify(result)

@booking_api.route("/booking/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        result = {
            "BookingID": booking.BookingID,
            "UserID": booking.UserID,
            "ScooterID": booking.ScooterID,
            "Time": booking.Time.strftime("%Y-%m-%d %H:%M:%S"),
            "Status": booking.Status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404
    
@booking_api.route("/bookings", methods=["POST"])
def add_booking():
    data = request.json
    new_booking = Booking(
        UserID=data.get("UserID"),
        ScooterID=data.get("ScooterID"),
        Time=data.get("Time"),
        Status=data.get("Status")
    )

    db.session.add(new_booking)
    db.session.commit()

    result = {
        "BookingID": new_booking.BookingID,
        "UserID": new_booking.UserID,
        "ScooterID": new_booking.ScooterID,
        "Time": new_booking.Time.strftime("%Y-%m-%d %H:%M:%S"),
        "Status": new_booking.Status
    }
    return jsonify(result), 201


@booking_api.route("/booking/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        data = request.json
        booking.UserID = data.get("UserID")
        booking.ScooterID = data.get("ScooterID")
        booking.Time = data.get("Time")
        booking.Status = data.get("Status")

        db.session.commit()

        result = {
            "BookingID": booking.BookingID,
            "UserID": booking.UserID,
            "ScooterID": booking.ScooterID,
            "Time": booking.Time.strftime("%Y-%m-%d %H:%M:%S"),
            "Status": booking.Status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404


@booking_api.route("/booking/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        result = {
            "BookingID": booking.BookingID,
            "UserID": booking.UserID,
            "ScooterID": booking.ScooterID,
            "Time": booking.Time.strftime("%Y-%m-%d %H:%M:%S"),
            "Status": booking.Status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404