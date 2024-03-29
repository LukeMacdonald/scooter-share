import datetime
from flask import Blueprint, request, jsonify
from database.models import Booking, BookingState
from database.database_manager import db

booking_api = Blueprint("booking_api", __name__)


def parse_datetime(date: str):
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def parse_date(date: str):
    return datetime.datetime.strptime(date, "%Y-%m-%d")


@booking_api.route("/bookings", methods=["GET"])
def get_all():
    """
    Retrieve all bookings from the database.

    Returns:
        list: A list of booking objects in JSON format.
    """
    bookings = Booking.query.all()
    return [booking.as_json() for booking in bookings]


@booking_api.route("/booking/<int:booking_id>", methods=["GET"])
def get(booking_id):
    """
    Retrieve a booking by its ID from the database.

    Args:
        booking_id (int): The ID of the booking to retrieve.

    Returns:
        dict: A dictionary representing the booking object in JSON format, or None if not found.
    """
    booking = Booking.query.get(booking_id)
    if booking:
        return booking.as_json()
    else:
        return jsonify({"message": "Booking not found"}), 404


@booking_api.route("/bookings", methods=["POST"])
def post():
    """
    Add a new booking to the database.

    Args:
        data (dict): A dictionary containing booking data.

    Returns:
        dict: A dictionary representing the newly created booking object in JSON format.
    """
    data = request.json
    new_booking = Booking(
        user_id=data["user_id"],
        scooter_id=data["scooter_id"],
        date=parse_date(data["date"]),
        start_time=parse_datetime(data["start_time"]),
        end_time=parse_datetime(data["end_time"]),
        status=data["status"],
        event_id=data["event_id"]
    )

    db.session.add(new_booking)
    db.session.commit()

    return new_booking.as_json()


@booking_api.route("/booking/id/<int:booking_id>", methods=["PUT"])
def update(booking_id):
    """
    Update an existing booking in the database.

    Args:
        booking_id (int): The ID of the booking to update.
        new_booking (dict): A dictionary containing updated booking data.

    Returns:
        dict: A dictionary representing the updated booking object in JSON format, or None if not found.
    """
    new_booking = request.json
    booking = Booking.query.get(booking_id)
    if booking:
        booking.user_id = new_booking["user_id"]
        booking.scooter_id = new_booking["scooter_id"]
        booking.start_time = parse_datetime(new_booking["start_time"])
        booking.end_time = parse_datetime(new_booking["end_time"])
        booking.date = parse_date(new_booking["date"])
        booking.status = new_booking["status"]
        db.session.commit()
        return booking.as_json()
    else:
        return jsonify({"message": "Booking not found"}), 404


@booking_api.route("/booking/status/<int:booking_id>", methods=["PUT"])
def update_status(booking_id):
    """
    Update an existing booking in the database.

    Args:
        booking_id (int): The ID of the booking to update.
        new_booking (dict): A dictionary containing updated booking data.

    Returns:
        dict: A dictionary representing the updated booking object in JSON format, or None if not found.
    """
    data = request.json
    status = data["status"]
    booking = Booking.query.get(booking_id)

    if booking:
        booking.status = status
        db.session.commit()
        return booking.as_json()
    else:
        return jsonify({"message": "Booking not found"}), 404


@booking_api.route("/booking/<int:booking_id>", methods=["DELETE"])
def delete(booking_id):
    """
    Delete a booking from the database.

    Args:
        booking_id (int): The ID of the booking to delete.

    Returns:
        dict: A dictionary representing the deleted booking object in JSON format, or None if not found.
    """
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking successfully deleted"}), 200
    else:
        return jsonify({"message": "Booking not found"}), 404


@booking_api.route("/bookings/user/<int:user_id>", methods=["GET"])
def get_by_user(user_id):
    """
    Retrieve bookings associated with a specific user from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of booking objects in JSON format associated with the specified user.
    """
    bookings = Booking.query.filter_by(user_id=user_id)
    return [booking.as_json() for booking in bookings]


@booking_api.route("/bookings/status/<string:status>", methods=["GET"])
def get_by_status(status):
    bookings = Booking.query.filter_by(status=status)
    return [booking.as_json() for booking in bookings]


class BookingAPI:

    def get_by_user_and_scooter(user_id: int, scooter_id: int):
        booking = Booking.query.filter_by(
            user_id=user_id,
            scooter_id=scooter_id,
            status=BookingState.ACTIVE.value
        ).first()
        return booking if booking else None

    def update(booking_id: int, updated_booking: Booking):
        """
        Update an existing booking in the database.

        Args:
            booking_id (int): The ID of the booking to update.
            updated_booking (dict): A dictionary containing updated booking data.

        Returns:
            dict: A dictionary representing the updated booking object in JSON format, or None if not found.
        """

        booking = Booking.query.get(booking_id)

        if booking:
            booking.user_id = updated_booking.user_id
            booking.scooter_id = updated_booking.scooter_id
            booking.start_time = updated_booking.start_time
            booking.end_time = updated_booking.end_time
            booking.date = updated_booking.date
            booking.status = updated_booking.status
            db.session.commit()

            return booking
        else:
            return jsonify({"message": "Booking not found"}), 404
