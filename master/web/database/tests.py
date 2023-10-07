import unittest
from datetime import datetime
from master.database.database_manager import db
from master.web.app import create_master_app
from master.database.models import Booking, User, UserType, Scooter, ScooterStatus, Repairs, RepairStatus, Transaction

class APITestCase(unittest.TestCase):
    """
    Test case for the booking API endpoints.
    """
    #todo: Refractor Unit Testing for API
    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        self.app = create_master_app(True)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.app.app_context().push()
        db.create_all()
        
    def convert_date(self, date):
        """
        Convert a string date to a formatted date string.
        
        Args:
            str (str): String representing a date in "%Y-%m-%d %H:%M:%S" format.

        Returns:
            str: Formatted date string.
        """
        formatted = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return formatted.strftime("%a %d %b, %H:%M, %Y")

    def tearDown(self):
        """
        Clean up the test environment after each test case.
        """
        db.session.remove()
        db.drop_all()

    # Booking API Unit Tests 
    def test_get_all_bookings(self):
        """
        Test the endpoint for retrieving all bookings from the database.
        """
        booking1 = Booking(user_id=1, scooter_id=1, date=datetime(2023, 9, 29), start_time=datetime(2023, 9, 29, 12, 0), end_time=datetime(2023, 9, 29, 12, 30), status="active", event_id=1)
        booking2 = Booking(user_id=2, scooter_id=3, date=datetime(2023, 9, 30), start_time=datetime(2023, 9, 29, 14, 30), end_time=datetime(2023, 9, 29, 15, 30), status="cancelled", event_id=2)
        
        db.session.add_all([booking1, booking2])
        db.session.commit()
        
        response = self.client.get('/bookings')
        
        expected_data = [
            {'date': '2023-09-29', 'end_time': 'Fri 29 Sep, 12:30, 2023', 'id': 1, 'scooter_id': 1, 'start_time': 'Fri 29 Sep, 12:00, 2023', 'status': 'active', 'user_id': 1},
            {'date': '2023-09-30', 'end_time': 'Fri 29 Sep, 15:30, 2023', 'id': 2, 'scooter_id': 3, 'start_time': 'Fri 29 Sep, 14:30, 2023', 'status': 'cancelled', 'user_id': 2}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)
    
    def test_get_all_no_bookings(self):
        """
        Test the endpoint for retrieving all bookings from the database.
        """  
        response = self.client.get('/bookings')
        
        expected_data = []
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)
     
    def test_get_booking_by_id_successful(self):
        """
        Test the endpoint for retrieving a specific booking by its ID when the booking exists.
        """
        booking1 = Booking(user_id=1, scooter_id=1, date=datetime(2023, 9, 29),
                           start_time=datetime(2023, 9, 29, 12, 0),
                           end_time=datetime(2023, 9, 29, 12, 30),
                           status="active", event_id=1)
        db.session.add_all([booking1])
        db.session.commit()
        response = self.client.get('/booking/1')

        expected_data = {
            'date': '2023-09-29',
            'end_time': 'Fri 29 Sep, 12:30, 2023',
            'id': 1,
            'scooter_id': 1,
            'start_time': 'Fri 29 Sep, 12:00, 2023',
            'status': 'active',
            'user_id': 1
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)
        
    def test_get_booking_by_id_failure(self):
        """
        Test the endpoint for retrieving a specific booking by its ID when the booking does not exist.
        """
        response = self.client.get('/booking/1')
        expected_data = {
            'message': 'Booking not found', 
        }
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)
    
    def test_create_booking_successful(self):
        """
        Test the endpoint for creating a new booking in the database. 
        """
        booking_data = {
            'user_id': 3,
            'scooter_id': 4,
            'date': '2023-10-01',
            'start_time': '2023-10-01 10:00:00',
            'end_time': '2023-10-01 12:00:00',
            'status': 'active',
            'event_id': 3
        }

        response = self.client.post('/bookings', json=booking_data)
        
        self.assertEqual(response.status_code, 200)

        created_booking_data = response.json
        print(created_booking_data)
        self.assertEqual(created_booking_data['user_id'], booking_data['user_id'])
        self.assertEqual(created_booking_data['scooter_id'], booking_data['scooter_id'])
        self.assertEqual(created_booking_data['date'], booking_data['date'])
        self.assertEqual(created_booking_data['start_time'], self.convert_date(booking_data["start_time"]))
        self.assertEqual(created_booking_data['end_time'], self.convert_date(booking_data["end_time"]))
        self.assertEqual(created_booking_data['status'], booking_data['status'])

    def test_update_booking_successful(self):
        """
        Test the endpoint for updating an existing booking in the database.
        """
        booking_data = {
            'user_id': 3,
            'scooter_id': 4,
            'date': '2023-10-01',
            'start_time': '2023-10-01 10:00:00',
            'end_time': '2023-10-01 12:00:00',
            'status': 'active',
            'event_id': 3
        }

        # Create a new booking
        response = self.client.post('/bookings', json=booking_data)
        created_booking_data = response.json

        # Update the booking with new data
        updated_booking_data = {
            'user_id': 3,
            'scooter_id': 4,
            'date': '2023-10-01',
            'start_time': '2023-10-01 12:00:00',
            'end_time': '2023-10-01 14:00:00',   
            'status': 'active',                   
            'event_id': 3
        }

        # Make PUT request to update the booking
        response = self.client.put(f'/booking/id/{created_booking_data["id"]}', json=updated_booking_data)

        # Assert the response and updated booking data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user_id'], updated_booking_data['user_id'])
        self.assertEqual(response.json['scooter_id'], updated_booking_data['scooter_id'])
        self.assertEqual(response.json['date'], updated_booking_data['date'])
        self.assertEqual(response.json['status'], updated_booking_data['status'])
        self.assertEqual(response.json['start_time'], self.convert_date(updated_booking_data['start_time']))
        self.assertEqual(response.json['end_time'], self.convert_date(updated_booking_data['end_time']))

    def test_update_booking_status_successful(self):
        """
        Test the endpoint for updating the status of an existing booking in the database.
        """
        booking_data = {
            'user_id': 3,
            'scooter_id': 4,
            'date': '2023-10-01',
            'start_time': '2023-10-01 10:00:00',
            'end_time': '2023-10-01 12:00:00',
            'status': 'active',
            'event_id': 3
        }

        # Create a new booking
        response = self.client.post('/bookings', json=booking_data)
        created_booking_data = response.json

        # Update the booking status
        updated_status = {
            'status': 'cancelled'
        }

        # Make PUT request to update the booking status
        response = self.client.put(f'/booking/status/{created_booking_data["id"]}', json=updated_status)

        # Assert the response and updated status
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], updated_status['status'])

    def test_delete_booking_successful(self):
        """
        Test the endpoint for deleting an existing booking from the database.
        """
        booking_data = {
            'user_id': 3,
            'scooter_id': 4,
            'date': '2023-10-01',
            'start_time': '2023-10-01 10:00:00',
            'end_time': '2023-10-01 12:00:00',
            'status': 'active',
            'event_id': 3
        }

      
        response = self.client.post('/bookings', json=booking_data)
        created_booking_data = response.json

       
        response = self.client.delete(f'/booking/{created_booking_data["id"]}')

       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Booking successfully deleted')
    
    def test_delete_booking_failure(self):
        """
        Test the endpoint for deleting an non-existing booking from the database.
        """
            
        response = self.client.delete(f'/booking/999')

       
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Booking not found')  #
    
    def test_get_bookings_by_user_successful(self):
        """
        Test the endpoint for retrieving bookings associated with a specific user.
        """

        user_id = 1
        booking1 = Booking(user_id=user_id, scooter_id=1, date=datetime(2023, 9, 29),
                        start_time=datetime(2023, 9, 29, 12, 0),
                        end_time=datetime(2023, 9, 29, 12, 30),
                        status="active", event_id=1)
        booking2 = Booking(user_id=user_id, scooter_id=2, date=datetime(2023, 9, 30),
                        start_time=datetime(2023, 9, 30, 14, 0),
                        end_time=datetime(2023, 9, 30, 15, 0),
                        status="active", event_id=2)
        
        db.session.add_all([booking1, booking2])
        db.session.commit()

        response = self.client.get(f'/bookings/user/{user_id}')

        
        self.assertEqual(response.status_code, 200)
        retrieved_bookings = response.json
        self.assertEqual(len(retrieved_bookings), 2)  
        self.assertEqual(retrieved_bookings[0]['user_id'], user_id)
        self.assertEqual(retrieved_bookings[1]['user_id'], user_id)
      
    def test_get_bookings_by_user_not_found(self):
        """
        Test the endpoint for retrieving bookings associated with a user when the user does not exist.
        """
        non_existing_user_id = 999  # Assuming this user ID does not exist in the database
        response = self.client.get(f'/bookings/user/{non_existing_user_id}')

        # Assert the response and error message
        self.assertEqual(response.status_code, 200)
        expected_response = []
        self.assertEqual(response.json, expected_response)
    
    # User API Unit Tests
    def test_get_all_users_nonexist(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) == 0)
    
    def test_get_all_users(self):
        customer = User(username='customer1', password='password', email='customer@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        engineer = User(username='engineer1', password='password', email='engineer@example.com',
                    first_name='Engineer', last_name='User', role=UserType.ENGINEER.value,phone_number="0429825982",balance=0.0)
        admin = User(username='admin1', password='password', email='admin@example.com',
                    first_name='Admin', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        db.session.add_all([customer,engineer, admin])
        db.session.commit()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) == 3)
    
    def test_get_user_by_id_successful(self):
        customer = User(username='customer1', password='password', email='customer@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add(customer)
        db.session.commit()

        response = self.client.get(f'/user/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'customer1')
    
    def test_get_user_by_email_successful(self):
        email = 'customer@example.com'
        customer = User(username='customer1', password='password', email=email,
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add(customer)
        db.session.commit()

        response = self.client.get(f'/user/email/{email}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'customer1')
    
    def test_get_user_by_email_failure(self):
        
        email = 'customer@example.com'
        customer = User(username='customer1', password='password', email=email,
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add(customer)
        db.session.commit()
        
        incorrect_email = 'customer1@example.com'


        response = self.client.get(f'/user/email/{incorrect_email}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'User not found')

    def test_get_user_by_role_engineer(self):
        engineer = User(username='engineer1', password='password', email='engineer1@example.com',
                    first_name='Customer', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)
        engineer2 = User(username='engineer2', password='password', email='engineer2@example.com',
                    first_name='Engineer', last_name='User', role=UserType.ENGINEER.value,phone_number="0429825982",balance=0.0)
        engineer3 = User(username='engineer3', password='password', email='engineer3@example.com',
                    first_name='Admin', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)
        admin = User(username='admin1', password='password', email='admin@example.com',
                    first_name='Admin', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        customer = User(username='customer1', password='password', email='customer@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add_all([engineer,engineer2, engineer3, admin, customer])
        db.session.commit()
        
        response = self.client.get(f'/user/role/{UserType.ENGINEER.value}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
     
    def test_get_user_by_role_customer(self):
        engineer = User(username='engineer1', password='password', email='engineer1@example.com',
                    first_name='Customer', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)
        engineer2 = User(username='engineer2', password='password', email='engineer2@example.com',
                    first_name='Engineer', last_name='User', role=UserType.ENGINEER.value,phone_number="0429825982",balance=0.0)
       
        admin = User(username='admin1', password='password', email='admin@example.com',
                    first_name='Admin', last_name='User', role=UserType.ADMIN.value, phone_number="0429825982",balance=0.0)
        
        customer = User(username='customer1', password='password', email='customer@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        customer2 = User(username='customer2', password='password', email='customer2@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add_all([engineer,engineer2, customer2, admin, customer])
        db.session.commit()
        
        response = self.client.get(f'/user/role/{UserType.CUSTOMER.value}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
    
    def test_get_user_by_role_admin(self):
        engineer = User(username='engineer1', password='password', email='engineer1@example.com',
                    first_name='Customer', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)
        engineer2 = User(username='engineer2', password='password', email='engineer2@example.com',
                    first_name='Engineer', last_name='User', role=UserType.ENGINEER.value,phone_number="0429825982",balance=0.0)
       
        admin = User(username='admin1', password='password', email='admin@example.com',
                    first_name='Admin', last_name='User', role=UserType.ADMIN.value, phone_number="0429825982",balance=0.0)
        
        customer = User(username='customer1', password='password', email='customer@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        customer2 = User(username='customer2', password='password', email='customer2@example.com',
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add_all([engineer,engineer2, customer2, admin, customer])
        db.session.commit()
        
        response = self.client.get(f'/user/role/{UserType.ADMIN.value}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        
    def test_get_user_by_id_failure(self):
        response = self.client.get('/user/id/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user_successful(self):
        user_data = {
          'username':'engineer1', 
          'password':'password', 
          'email':'engineer@example.com',
          'first_name':'Engineer', 
          'last_name':'User', 
          'role':UserType.ENGINEER.value,
          'phone_number':"0429825982",
          'balance': 0.0
        }
        response = self.client.post('/user', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'engineer1')

    def test_update_user_successful(self):
        email = 'customer@example.com'
        customer = User(username='customer1', password='password', email=email,
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add(customer)
        db.session.commit()
        
        
        user = self.client.get(f"/user/email/{email}")
        
        user_json = user.json

        user_json['first_name'] = 'Updated'
        user_json['last_name'] = 'NewLastName'
        
        response = self.client.put(f'/user/{ user_json["id"]}', json= user_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], user_json['first_name'])
        self.assertEqual(response.json['last_name'], user_json['last_name'])
        self.assertEqual(response.json['role'], UserType.CUSTOMER.value)

    def test_delete_user_successful(self):
        email = 'customer@example.com'
        customer = User(username='customer1', password='password', email=email,
                    first_name='Customer', last_name='User', role=UserType.CUSTOMER.value, phone_number="0429825982",balance=0.0)
        
        db.session.add(customer)
        db.session.commit()
        
        user = self.client.get(f"/user/email/{email}").json
        
    

        response = self.client.delete(f'/user/{user["id"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'customer1')

    def test_delete_user_failure(self):
        response = self.client.delete('/user/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'User not found')

    def test_get_engineer_emails(self):
        engineer = User(username='engineer1', password='password', email='engineer1@example.com',
                    first_name='Customer', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)
        engineer2 = User(username='engineer2', password='password', email='engineer2@example.com',
                    first_name='Engineer', last_name='User', role=UserType.ENGINEER.value,phone_number="0429825982",balance=0.0)
        engineer3 = User(username='engineer3', password='password', email='engineer3@example.com',
                    first_name='Admin', last_name='User', role=UserType.ENGINEER.value, phone_number="0429825982",balance=0.0)

        db.session.add_all([engineer,engineer2, engineer3])
        db.session.commit()
        
        response = self.client.get('/users/engineers/emails')
        emails = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(emails), 3)
        self.assertEqual(emails[0], 'engineer1@example.com')
        self.assertEqual(emails[1], 'engineer2@example.com')
        self.assertEqual(emails[2], 'engineer3@example.com')
    
    def test_get_engineer_emails_nonexist(self):
        response = self.client.get('/users/engineers/emails')
        emails = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(emails), 0)

    # Scooter API Unit Tests
    def test_create_scooter_successful(self):
        scooter_data = {
            'make': 'ScooterX',
            'longitude': 123.456,
            'latitude': 78.910,
            'cost_per_time': 5.0,
            'colour': 'Red',
            'remaining_power':75.0,
            'status': ScooterStatus.AVAILABLE.value
        }

        response = self.client.post('/scooter', json=scooter_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['make'], scooter_data['make'])
        self.assertEqual(response.json['longitude'], scooter_data['longitude'])
        self.assertEqual(response.json['latitude'], scooter_data['latitude'])
        self.assertEqual(response.json['cost_per_time'], scooter_data['cost_per_time'])
        self.assertEqual(response.json['colour'], scooter_data['colour'])
        self.assertEqual(response.json['status'], ScooterStatus.AVAILABLE.value)
    
    def test_create_scooter_invalid_data(self):
        scooter_data = {
            'make': 'ScooterX',
            'longitude': 123.456,
            'cost_per_time': 5.0,
            'colour': 'Red'
        }

        response = self.client.post('/scooter', json=scooter_data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_scooters(self):
        scooter1 = Scooter(make='ScooterX', longitude=123.456, latitude=78.910, remaining_power=100.0,
                           cost_per_time=5.0, status=ScooterStatus.AVAILABLE.value, colour='Red')
        scooter2 = Scooter(make='ScooterY', longitude=45.678, latitude=90.123, remaining_power=80.0,
                           cost_per_time=4.0, status=ScooterStatus.OCCUPYING.value, colour='Blue')

        db.session.add_all([scooter1, scooter2])
        db.session.commit()

        response = self.client.get('/scooters/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['make'], 'ScooterX')
        self.assertEqual(response.json[1]['make'], 'ScooterY')

    def test_get_scooter_by_id_successful(self):
        scooter = Scooter(make='ScooterX', longitude=123.456, latitude=78.910, remaining_power=100.0,
                          cost_per_time=5.0, status=ScooterStatus.AVAILABLE.value, colour='Red')
        db.session.add(scooter)
        db.session.commit()

        response = self.client.get('/scooter/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['make'], 'ScooterX')

    def test_get_scooter_by_id_failure(self):
        response = self.client.get('/scooter/id/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Scooter not found')

    def test_get_scooters_by_status(self):
        scooter1 = Scooter(make='ScooterX', longitude=123.456, latitude=78.910, remaining_power=100.0,
                           cost_per_time=5.0, status=ScooterStatus.AVAILABLE.value, colour='Red')
        scooter2 = Scooter(make='ScooterY', longitude=45.678, latitude=90.123, remaining_power=80.0,
                           cost_per_time=4.0, status=ScooterStatus.OCCUPYING.value, colour='Blue')

        db.session.add_all([scooter1, scooter2])
        db.session.commit()

        response = self.client.get(f'/scooters/status/{ScooterStatus.AVAILABLE.value}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['make'], 'ScooterX')

    def test_get_scooters_by_invalid_status(self):
        response = self.client.get('/scooters/status/INVALID_STATUS')
        self.assertEqual(response.status_code, 400)

    def test_update_scooter_successful(self):
        original_scooter_data = {
            'make': 'ScooterX',
            'longitude': 123.456,
            'latitude': 78.910,
            'remaining_power': 80.0,
            'cost_per_time': 4.0,
            'status': ScooterStatus.AVAILABLE.value,
            'colour': 'Blue'
        }
     
        scooter = Scooter(make=original_scooter_data['make'], longitude=original_scooter_data['longitude'], latitude=original_scooter_data['latitude'], remaining_power=original_scooter_data['remaining_power'],
                          cost_per_time=original_scooter_data['cost_per_time'], status=original_scooter_data['status'], colour=original_scooter_data['colour'])
        
        db.session.add(scooter)
        
        db.session.commit()

        updated_scooter_data = {
            'longitude': 45.678,
            'latitude': 90.123,
            'remaining_power': 80.0,
            'status': ScooterStatus.OCCUPYING.value,
        }
        
        scooter_data = self.client.get("/scooter/id/1").json
   
    
        scooter_data['status'] = updated_scooter_data['status']
        scooter_data['longitude'] = updated_scooter_data['longitude']
        scooter_data['latitude'] = updated_scooter_data['latitude']
        scooter_data['remaining_power'] = updated_scooter_data['remaining_power']
        
        response = self.client.put('/scooter/id/1', json=scooter_data)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['make'], original_scooter_data['make'])
        self.assertEqual(response.json['longitude'], updated_scooter_data['longitude'])
        self.assertEqual(response.json['latitude'], updated_scooter_data['latitude'])
        self.assertEqual(response.json['remaining_power'], updated_scooter_data['remaining_power'])
        self.assertEqual(response.json['cost_per_time'], original_scooter_data['cost_per_time'])
        self.assertEqual(response.json['status'], updated_scooter_data['status'])
        self.assertEqual(response.json['colour'], original_scooter_data['colour'])

    def test_update_scooter_failure(self):
        updated_scooter_data = {
            'make': 'ScooterY',
            'longitude': 45.678,
            'latitude': 90.123,
            'remaining_power': 80.0,
            'cost_per_time': 4.0,
            'status': ScooterStatus.OCCUPYING.value,
            'colour': 'Blue'
        }

        response = self.client.put('/scooter/id/1', json=updated_scooter_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Scooter not found')

    def test_update_scooter_status_successful(self):
        scooter = Scooter(make='ScooterX', longitude=123.456, latitude=78.910, remaining_power=100.0,
                          cost_per_time=5.0, status=ScooterStatus.AVAILABLE.value, colour='Red')
        db.session.add(scooter)
        db.session.commit()

        updated_status_data = {
            'status': ScooterStatus.OCCUPYING.value
        }

        response = self.client.put('/scooter/status/1', json=updated_status_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], ScooterStatus.OCCUPYING.value)

    def test_update_scooter_status_failure(self):
        updated_status_data = {
            'status': 'INVALID_STATUS'
        }

        response = self.client.put('/scooter/status/1', json=updated_status_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid status provided')

    # Repair API Unit Tests
    def test_get_all_repairs(self):
        """
        Test the endpoint for retrieving all repair records from the database.
        """
        repair1 = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        repair2 = Repairs(scooter_id=2, report='Issue 2', status=RepairStatus.COMPLETED.value)
        
        db.session.add_all([repair1, repair2])
        db.session.commit()
        
        response = self.client.get('/repairs/all')
        
        expected_data = [
            {'repair_id': 1, 'scooter_id': 1, 'report': 'Issue 1', 'status': RepairStatus.PENDING.value},
            {'repair_id': 2, 'scooter_id': 2, 'report': 'Issue 2', 'status': RepairStatus.COMPLETED.value}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_repair_by_id(self):
        """
        Test the endpoint for retrieving a specific repair record by its ID when the repair exists.
        """
        repair = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        db.session.add(repair)
        db.session.commit()

        response = self.client.get('/repair/1')

        expected_data = {
            'repair_id': 1,
            'scooter_id': 1,
            'report': 'Issue 1',
            'status': RepairStatus.PENDING.value
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_repair_by_id_failure(self):
        """
        Test the endpoint for retrieving a specific repair record by its ID when the repair does not exist.
        """
        response = self.client.get('/repair/1')
        expected_data = {
            'message': 'Repair not found'
        }
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)

    def test_create_repair(self):
        """
        Test the endpoint for creating a new repair record in the database.
        """
        repair_data = {
            'scooter_id': 1,
            'report': 'Issue 1',
            'status': RepairStatus.PENDING.value
        }

        response = self.client.post('/repair', json=repair_data)
        self.assertEqual(response.status_code, 200)

        created_repair_data = response.json
        expected_data = {
            'repair_id': 1,
            'scooter_id': 1,
            'report': 'Issue 1',
            'status': RepairStatus.PENDING.value
        }
        self.assertEqual(created_repair_data, expected_data)

    def test_update_repair(self):
        """
        Test the endpoint for updating an existing repair record in the database.
        """
        repair = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        db.session.add(repair)
        db.session.commit()

        updated_repair_data = {
            'scooter_id': 2,
            'report': 'Updated Issue',
            'status': RepairStatus.COMPLETED.value
        }

        response = self.client.put('/repair/id/1', json=updated_repair_data)
        self.assertEqual(response.status_code, 200)

        updated_data = response.json
        expected_data = {
            'repair_id': 1,
            'scooter_id': 2,
            'report': 'Updated Issue',
            'status': RepairStatus.COMPLETED.value
        }
        self.assertEqual(updated_data, expected_data)

    def test_delete_repair(self):
        """
        Test the endpoint for deleting an existing repair record from the database.
        """
        repair = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        db.session.add(repair)
        db.session.commit()

        response = self.client.delete('/repair/1')
        expected_data = {
            'repair_id': 1,
            'scooter_id': 1,
            'report': 'Issue 1',
            'status': RepairStatus.PENDING.value
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_delete_repair_failure(self):
        """
        Test the endpoint for deleting a non-existing repair record from the database.
        """
        response = self.client.delete('/repair/1')
        expected_data = {
            'message': 'Repair not found'
        }
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)

    def test_get_pending_repairs(self):
        """
        Test the endpoint for retrieving all pending repair records from the database.
        """
        repair1 = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        repair2 = Repairs(scooter_id=2, report='Issue 2', status=RepairStatus.COMPLETED.value)

        db.session.add_all([repair1, repair2])
        db.session.commit()

        response = self.client.get('/repairs/pending')

        expected_data = [
            {'repair_id': 1, 'scooter_id': 1, 'report': 'Issue 1', 'status': RepairStatus.PENDING.value}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_update_repair_status(self):
        """
        Test the endpoint for updating the status of an existing repair record in the database.
        """
        repair = Repairs(scooter_id=1, report='Issue 1', status=RepairStatus.PENDING.value)
        db.session.add(repair)
        db.session.commit()

        updated_status_data = {
            'status': RepairStatus.COMPLETED.value
        }

        response = self.client.put('/repair/status/1', json=updated_status_data)
        self.assertEqual(response.status_code, 200)

        updated_data = response.json
        expected_data = {
            'repair_id': 1,
            'scooter_id': 1,
            'report': 'Issue 1',
            'status': RepairStatus.COMPLETED.value
        }
        self.assertEqual(updated_data, expected_data)

    def test_update_repair_status_failure(self):
        """
        Test the endpoint for updating the status of a non-existing repair record in the database.
        """
        updated_status_data = {
            'status': RepairStatus.COMPLETED.value
        }

        response = self.client.put('/repair/status/1', json=updated_status_data)
        expected_data = {
            'message': 'Repair not found'
        }
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)
    
    # Transaction API Unit Tests
    def test_get_all_transactions(self):
        """
        Test the endpoint for retrieving all transactions from the database.
        """
        transaction1 = Transaction(user_id=1, amount=100)
        transaction2 = Transaction(user_id=2, amount=200)

        db.session.add_all([transaction1, transaction2])
        db.session.commit()

        response = self.client.get('/transactions/all')

        expected_data = [
            {'id': 1, 'user_id': 1, 'amount': 100},
            {'id': 2,'user_id': 2, 'amount': 200}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_transaction_by_id(self):
        """
        Test the endpoint for retrieving a transaction by its ID from the database.
        """
        transaction = Transaction(user_id=1, amount=100)
        db.session.add(transaction)
        db.session.commit()

        response = self.client.get('/transaction/1')

        expected_data = {'id': 1,'user_id': 1, 'amount': 100}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_non_existing_transaction(self):
        """
        Test the endpoint for retrieving a non-existing transaction by its ID from the database.
        """
        response = self.client.get('/transaction/1')
        expected_data = {'message': 'Transaction not found'}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_data)

    def test_create_new_transaction(self):
        """
        Test the endpoint for creating a new transaction in the database.
        """
        new_transaction_data = {'user_id': 1, 'amount': 300}

        response = self.client.post('/transaction', json=new_transaction_data)

        expected_data = {'id': 1,'user_id': 1, 'amount': 300}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_transactions_by_user(self):
        """
        Test the endpoint for retrieving all transactions for a specific user from the database.
        """
        transaction1 = Transaction(user_id=1, amount=100)
        transaction2 = Transaction(user_id=1, amount=200)

        db.session.add_all([transaction1, transaction2])
        db.session.commit()

        response = self.client.get('/transactions/user/1')

        expected_data = [
            {'id': 1,'user_id': 1, 'amount': 100},
            {'id': 2,'user_id': 1, 'amount': 200}
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)

    def test_get_transactions_for_non_existing_user(self):
        """
        Test the endpoint for retrieving transactions for a non-existing user from the database.
        """
        response = self.client.get('/transactions/user/1')
        expected_data = []
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_data)