from database.database_manager import db
from sqlalchemy.orm import relationship

class User(db.Model):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('customer', 'engineer', 'admin'), nullable=False)
    phone_number = db.Column(db.String(12))

class Scooter(db.Model):
    """
    Represents a scooter in the system.
    """
    __tablename__ = 'scooters'

    ScooterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Make = db.Column(db.String(100), nullable=False)
    Longitude = db.Column(db.Float(precision=6), nullable=False)  
    Latitude = db.Column(db.Float(precision=6), nullable=False)  
    RemainingPower = db.Column(db.Float(precision=2), nullable=False)
    CostPerTime = db.Column(db.Float(precision=2), nullable=False)
    Status = db.Column(db.Enum('available', 'occupying', 'maintenance','repaired'), nullable=False)

class Booking(db.Model):
    """
    Represents a booking in the system.
    """
    __tablename__ = 'bookings'

    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ScooterID = db.Column(db.Integer, db.ForeignKey('scooters.ScooterID'), nullable=False)
    Time = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.Enum('active', 'completed', 'cancelled'), nullable=False)

    user = relationship('User')
    scooter = relationship('Scooter')

class Repairs(db.Model):
    """
    Represents a repair record in the system.
    """
    __tablename__ = 'repairs'

    RepairID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ScooterID = db.Column(db.Integer, db.ForeignKey('scooters.ScooterID'), nullable=False)
    Report = db.Column(db.String(255), nullable=False)
    Status = db.Column(db.Enum('active', 'completed'), nullable=False)

    scooter = relationship('Scooter')

class Balance(db.Model):
    """
    Represents the balance of a user in the system.
    """
    __tablename__ = 'balances'

    BalanceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Balance = db.Column(db.Float(precision=2), nullable=False)

    user = relationship('User')