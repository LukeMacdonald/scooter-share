import datetime
from master.database.models import *
def seed_data():
    """
    Seed data into the database if no data exists.
    """
    if not Scooter.query.first():
        scooter_data()
    if not User.query.first():
        user_data()
    if not Booking.query.first():
        booking_data()
    if not Repairs.query.first():
        repair_data()
    if not Transaction.query.first():
        transaction_data()

def seed_model(model_class, data_list):
    """
    Seed data into a specific database model.
    """
    if not model_class.query.first():
        for data in data_list:
            model = model_class(**data)
            db.session.add(model)
        db.session.commit()

def scooter_data():
    """
    Seed scooter data into the Scooter model.
    """
    data = [
        {
            "cost_per_time": 10.99,
            "latitude": -37.8136,
            "longitude": 144.963,
            "make": "InMotion AIR",
            "remaining_power": 75.5,
            "status": ScooterStatus.AVAILABLE.value,
            "colour": "black"
        },
        {
            "cost_per_time": 9.99,
            "latitude": -37.815,
            "longitude": 144.978,
            "make": "InMotion AIR Pro",
            "remaining_power": 85.0,
            "status": ScooterStatus.OCCUPYING.value,
            "colour": "grey"
        },
        {
            "cost_per_time": 12.5,
            "latitude": -37.807,
            "longitude": 144.981,
            "make": "Kaabo Sky 8S",
            "remaining_power": 35.25,
            "status": ScooterStatus.AWAITING_REPAIR.value,
            "colour": "red"
        },
        {
            "cost_per_time": 10.99,
            "latitude": -37.8078,
            "longitude": 144.984,
            "make": "Segway-Ninebot GT2",
            "remaining_power": 10.5,
            "status": ScooterStatus.AWAITING_REPAIR.value,
            "colour": "blue"
        },
        {
            "cost_per_time": 9.99,
            "latitude": -37.8183,
            "longitude": 144.965,
            "make": "Kaabo Wolf Warrior 11 GT",
            "remaining_power": 5.0,
            "status": ScooterStatus.OCCUPYING.value,
            "colour": "black"
        },
        {
            "cost_per_time": 12.5,
            "latitude": -37.8072,
            "longitude": 144.99,
            "make": "NIU KQI3 Sport",
            "remaining_power": 50.25,
            "status": ScooterStatus.AVAILABLE.value,
            "colour": "orange"
        }
    ]
    seed_model(Scooter, data)

def user_data():
    """
    Seed user data into the User model.
    """
    data = [
        {
            "username": "customer1",
            "password": "password",
            "email": "customer1@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": UserType.CUSTOMER.value,
            "phone_number": "0434 567 890",
            "balance": 100.0,
            "is_active": False
        },
        {
            "username": "LukeMacca123",
            "password": "password",
            "email": "lukemacdonald21@gmail.com",
            "first_name": "Luke",
            "last_name": "Macdonald",
            "role": UserType.ENGINEER.value,
            "phone_number": "047 6543 210",
            "balance":0.0,
            "is_active": False
        },
        {
            "username": "admin",
            "password": "admin",
            "email": "admin@gmail.com",
            "first_name": "Adam",
            "last_name": "Joe",
            "role": UserType.ADMIN.value,
            "phone_number": "049 6823 921",
            "balance": 0.0,
            "is_active": False
        }
    ]
    seed_model(User,data)

def booking_data():
    """
    Seed booking data into the Booking model.
    """
    data = [
        {
            "user_id": 1,
            "scooter_id": 1,
            "date": datetime.datetime(2023, 9, 29),
            "start_time": datetime.datetime(2023, 9, 29, 12, 0),
            "end_time": datetime.datetime(2023, 9, 29, 12, 30),
            "status": BookingState.ACTIVE.value,
            "event_id": 1
        },
        {
            "user_id": 2,
            "scooter_id": 3,
            "date": datetime.datetime(2023, 9, 30),
            "start_time": datetime.datetime(2023, 9, 29, 14, 30),
            "end_time": datetime.datetime(2023, 9, 29, 15, 30),
            "status": BookingState.COMPLETED.value,
            "event_id": 2
        }
    ]
    seed_model(Booking,data)

def repair_data():
    """
    Seed repair data into the Repairs model.
    """
    data = [
        {
            "scooter_id": 3,
            "report": "Damaged wheel",
            "status": RepairStatus.ACTIVE.value
        },
        {
            "scooter_id": 4,  
            "report": "Battery replacement",
            "status": RepairStatus.ACTIVE.value
        },
        {
            "scooter_id": 1,  
            "report": "Damaged Handle",
            "status": RepairStatus.COMPLETED.value
        },
    ]
    seed_model(Repairs,data)

def transaction_data():
    """
    Seed transaction data into the Transaction model.
    """
    data = [
        {
            "user_id": 1,  
            "amount": 50.0
        },
        {
            "user_id": 2, 
            "amount": 25.0
        },
    ]
    seed_model(Transaction, data)
    
