import master.agent_interface.app as app
import master.agent_interface.comms as comms
import unittest

@comms.action("hello", ["start"])
def hello(handler, request):
    handler.state = "greeted"
    return "Hello!"
@comms.action("goodbye", ["greeted"])
def goodbye(handler, request):
    handler.state = "start"
    return "Goodbye!"

class MockHandler:
    def __init__(self):
        self.state = "start"

class TestComms(unittest.TestCase):
    def test_states(self):
        handler = MockHandler()
        self.assertEqual("Hello!", comms.handle(handler, {"name": "hello"}))
        self.assertEqual("Goodbye!", comms.handle(handler, {"name": "goodbye"}))
        self.assertTrue("error" in comms.handle(handler, {"name": "goodbye"}))
