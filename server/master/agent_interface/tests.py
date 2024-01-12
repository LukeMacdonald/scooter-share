import logging
import master.agent_interface.app as app
import master.agent_interface.comms as comms
import master.database.config as config
from web.app import create_master_app
import threading
import unittest

# Disable logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Start server
app.app = create_master_app()
thread = threading.Thread(target=lambda: app.app.run(host="localhost", port=5000, threaded=True))
thread.daemon = True
thread.start()

# comms library unit tests

@comms.action("hello", ["start"])
def hello(handler, request):
    handler.state = "greeted"
    return "Hello!"
@comms.action("goodbye", ["greeted"])
def goodbye(handler, request):
    handler.state = "start"
    return "Goodbye!"
@comms.action("barf", ["start"])
def barf(handler, request):
    raise ValueError("Your mother was a hamster, and your father smelt of elderberries")

class MockHandler:
    def __init__(self, state="start"):
        self.state = state

class TestComms(unittest.TestCase):
    def test_states(self):
        handler = MockHandler()
        self.assertEqual("Hello!", comms.handle(handler, {"name": "hello"}))
        self.assertEqual("Goodbye!", comms.handle(handler, {"name": "goodbye"}))
        self.assertTrue("error" in comms.handle(handler, {"name": "goodbye"}))
    def test_raise(self):
        handler = MockHandler()
        self.assertTrue("error" in comms.handle(handler, {"name": "barf"}))

# Master server tests

class TestApp(unittest.TestCase):
    # Login
    def test_unauthorised(self):
        handler = MockHandler()
        self.assertEqual("Unauthorised", comms.handle(handler, {"name": "locations"}).get("error"))
    def test_customer_login(self):
        handler = MockHandler()
        comms.handle(handler, {"name": "login", "email": "customer1@gmail.com", "password": "password"})
        self.assertEqual("customer", handler.state)
    def test_bad_login(self):
        handler = MockHandler()
        comms.handle(handler, {"name": "login", "email": "john@john.com", "password": "1111"})
        self.assertEqual("start", handler.state)
    # Registration
    def test_register(self):
        handler = MockHandler()
        resp = comms.handle(handler,
                            {"name": "register",
                             "role": "customer",
                             "email": "bob@bob.com",
                             "username": "bob",
                             "password": "1111",
                             "phone_number": "0412345678",
                             "first_name": "Bob",
                             "last_name": "Bobsson"})
        self.assertTrue("user" in resp)
        self.assertEqual("customer", handler.state)
    def test_existing_register(self):
        handler = MockHandler()
        # This user already exists -- see master/database/seed.py
        resp = comms.handle(handler,
                            {"name": "register",
                             "role": "customer",
                             "email": "customer1@gmail.com",
                             "username": "bob",
                             "password": "1111",
                             "phone_number": "0412345678",
                             "first_name": "Bob",
                             "last_name": "Bobsson"})
        self.assertTrue("Email address already registered", resp.get("error"))
        self.assertEqual("start", handler.state)
