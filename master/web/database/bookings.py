from flask import Blueprint, request, jsonify
from master.database.models import Booking
from master.database.database_manager import db

booking_api = Blueprint("booking_api", __name__)

@booking_api.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    result = [
        {
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "scooter_id": booking.scooter_id,
            "time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
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
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "scooter_id": booking.scooter_id,
            "time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404
    
@booking_api.route("/bookings", methods=["POST"])
def add_booking():
    data = request.json
    print(f"Here: {data}")
    new_booking = Booking(
        user_id=data.get("user_id"),
        scooter_id=data.get("scooter_id"),
        date=data.get("date"),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
        status=data.get("status")
    )

    db.session.add(new_booking)
    db.session.commit()

    result = {
        "booking_id": new_booking.id,
        "user_id": new_booking.user_id,
        "scooter_id": new_booking.scooter_id,
        "date": new_booking.date.strftime("%Y-%m-%d %H:%M:%S"),
        "start_time": new_booking.start_time.strftime("%H:%M:%S"),
        "end_time": new_booking.end_time.strftime("%H:%M:%S"),
        "status": new_booking.status
    }
    return jsonify(result), 201

@booking_api.route("/booking/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        data = request.json
        booking.user_id = data.get("user_id")
        booking.scooter_id = data.get("scooter_id")
        booking.time = data.get("time")
        booking.status = data.get("status")

        db.session.commit()

        result = {
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "scooter_id": booking.scooter_id,
            "time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
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
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "scooter_id": booking.scooter_id,
            "time": booking.time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": booking.status
        }
        return jsonify(result)
    else:
        return jsonify({"message": "Booking not found"}), 404
