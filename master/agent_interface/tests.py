import master.agent_interface.app as app
import master.agent_interface.comms as comms
import master.database.config as config
from master.web.app import create_master_app
import unittest

app.app = create_master_app()

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
    def __init__(self):
        self.state = "start"

class TestComms(unittest.TestCase):
    def test_states(self):
        handler = MockHandler()
        self.assertEqual("Hello!", comms.handle(handler, {"name": "hello"}))
        self.assertEqual("Goodbye!", comms.handle(handler, {"name": "goodbye"}))
        self.assertTrue("error" in comms.handle(handler, {"name": "goodbye"}))
    def test_raise(self):
        handler = MockHandler()
        self.assertTrue("error" in comms.handle(handler, {"name": "barf"}))

class TestApp(unittest.TestCase):
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
