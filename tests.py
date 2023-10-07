import unittest
from datetime import datetime
from master.database.database_manager import db
from master.web.app import create_master_app
from master.database.models import Booking

class BookingAPITestCase(unittest.TestCase):
    """
    Test case for the booking API endpoints.
    """
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

if __name__ == '__main__':
    unittest.main()
