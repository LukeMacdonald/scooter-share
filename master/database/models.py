"""
Database Models

This module defines SQLAlchemy models representing various entities in the system,
such as users, scooters, bookings, repairs, and user balances.

"""
from enum import Enum
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from master.database.database_manager import db

class UserType(Enum):
    ADMIN = 'admin'
    ENGINEER = 'engineer'
    CUSTOMER = 'customer'

class ScooterStatus(Enum):
    AVAILABLE = 'available'
    OCCUPYING = 'occupying'
    AWAITING_REPAIR = 'awaiting repair'
    
class BookingState(Enum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    
class RepairStatus(Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed' 
    PENDING = 'pending'
    
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
    role = db.Column(db.Enum(UserType.CUSTOMER.value,UserType.ENGINEER.value,UserType.ADMIN.value), 
                     nullable=False, default=UserType.CUSTOMER.value)
    phone_number = db.Column(db.String(10))
    balance = db.Column(db.Float(precision=2), nullable=False)
    
    def __init__(self, username, password, email, first_name, last_name, role=UserType.CUSTOMER.value, phone_number=None, balance=0.0):
        self.username = username
        self.password = sha256_crypt.hash(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.phone_number = phone_number
        self.balance = balance

    def as_json(self):
        "A dictionary with all the values other than the password hash of this user."
        phone_number = self.phone_number if self.phone_number is not None else ""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'phone_number': phone_number,
            'balance': self.balance
        }

class Scooter(db.Model):
    """
    Represents a scooter in the system.
    """
    __tablename__ = 'scooters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)  
    latitude = db.Column(db.Float(precision=6), nullable=False)  
    remaining_power = db.Column(db.Float(precision=2), nullable=False)
    cost_per_time = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.Enum(ScooterStatus.AVAILABLE.value,ScooterStatus.AWAITING_REPAIR.value,ScooterStatus.OCCUPYING.value), 
                       nullable=False)
    colour = db.Column(db.String(100), nullable=False)

    def as_json(self):
        "A dictionary with all the values of this scooter."
        return {
            "scooter_id": self.id,
            "make": self.make,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "remaining_power": self.remaining_power,
            "cost_per_time": self.cost_per_time,
            "status": self.status,
            "colour": self.colour
        }

class Booking(db.Model):
    """
    Represents a booking in the system.
    """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooters.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(BookingState.ACTIVE.value,BookingState.CANCELLED.value,BookingState.COMPLETED.value), 
                       nullable=False)
    event_id = db.Column(db.String(100), nullable=False)

    user = relationship('User')
    scooter = relationship('Scooter')

    def as_json(self):
        "A dictionary with all the values of this booking."
        return {
            "id": self.id,
            "user_id": self.user_id,
            "scooter_id": self.scooter_id,
            "start_time": self.start_time.strftime("%a %d %b, %H:%M, %Y"),
            "end_time": self.end_time.strftime("%a %d %b, %H:%M, %Y"),
            "status": self.status,
            "date": self.date.strftime("%Y-%m-%d"),
        }

class Repairs(db.Model):
    """
    Represents a repair record in the system.
    """
    __tablename__ = 'repairs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scooter_id = db.Column(db.Integer, db.ForeignKey('scooters.id'), nullable=False)
    report = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(RepairStatus.ACTIVE.value,RepairStatus.COMPLETED.value, RepairStatus.PENDING.value), nullable=False)

    scooter = relationship('Scooter')

    def as_json(self):
        return {
            "repair_id": self.id,
            "scooter_id": self.scooter_id,
            "report": self.report,
            "status": self.status
        }

class Transaction(db.Model):
    """
    Represents the transactions of a user in the system.
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float(precision=2), nullable=False)

    user = relationship('User')

    def as_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount
        }
