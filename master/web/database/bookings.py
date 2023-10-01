from flask import Blueprint, request, jsonify
from master.database.models import Booking
from master.database.database_manager import db

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    result = [
        {
            "BookingID": booking.id,
            "UserID": booking.user_id,
            "ScooterID": booking.scooter_id,
            "Time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
        }
        for booking in bookings
    ]
    return jsonify(result)

@booking_api.route("/booking/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        result = {
            "BookingID": booking.id,
            "UserID": booking.user_id,
            "ScooterID": booking.scooter_id,
            "Time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404
    
@booking_api.route("/bookings", methods=["POST"])
def add_booking():
    data = request.json
    new_booking = Booking(
        user_id=data.get("UserID"),
        scooter_id=data.get("ScooterID"),
        time=data.get("Time"),
        status=data.get("status")
    )

    db.session.add(new_booking)
    db.session.commit()

    result = {
        "BookingID": new_booking.id,
        "UserID": new_booking.user_id,
        "ScooterID": new_booking.scooter_id,
        "Time": new_booking.time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": new_booking.status
    }
    return jsonify(result), 201


@booking_api.route("/booking/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        data = request.json
        booking.user_id = data.get("UserID")
        booking.scooter_id = data.get("ScooterID")
        booking.time = data.get("Time")
        booking.status = data.get("status")

        db.session.commit()

        result = {
            "BookingID": booking.id,
            "UserID": booking.user_id,
            "ScooterID": booking.scooter_id,
            "Time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
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
            "BookingID": booking.id,
            "UserID": booking.user_id,
            "ScooterID": booking.scooter_id,
            "Time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404
