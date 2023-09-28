"""
Database Models

This module defines SQLAlchemy models representing various entities in the system,
such as users, scooters, bookings, repairs, and user balances.

"""
from sqlalchemy.orm import relationship
from master.web.database.database_manager import db

class User(db.Model):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('customer', 'engineer', 'admin'), nullable=False)
    phone_number = db.Column(db.String(12))
    balance = db.Column(db.Float(precision=2), nullable=False)

class Scooter(db.Model):
    """
    Represents a scooter in the system.
    """
    __tablename__ = 'scooters'

    scooter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)  
    latitude = db.Column(db.Float(precision=6), nullable=False)  
    remaining_power = db.Column(db.Float(precision=2), nullable=False)
    cost_per_time = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.Enum('available', 'occupying', 'maintenance','repaired'), nullable=False)

class Booking(db.Model):
    """
    Represents a booking in the system.
    """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooters.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('active', 'completed', 'cancelled'), nullable=False)

    user = relationship('User')
    scooter = relationship('Scooter')

class Repairs(db.Model):
    """
    Represents a repair record in the system.
    """
    __tablename__ = 'repairs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooters.id'), nullable=False)
    report = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('active', 'completed'), nullable=False)

    scooter = relationship('Scooter')

class Transaction(db.Model):
    """
    Represents the transactions of a user in the system.
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)

    user = relationship('User')