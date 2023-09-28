from master.agent_interface import comms

"""
A little test of the state machine setup.
The client can only send hello then bye then hello then ...
"""

@comms.action("hello", ["start"])
def hello(handler, message):
    handler.state = "greeted"
    return "Hello!"
@comms.action("bye", ["greeted"])
def bye(handler, message):
    handler.state = "start"
    return "Goodbye!"

def run_agent_server():
    comms.run(12345)
