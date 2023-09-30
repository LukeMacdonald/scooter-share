import functools
import json
import logging
import socketserver
import threading

_actions = {}

def action(name, states):
    """
    A decorator to register an action for receiving a message with a given name.
    The connection must be in a state in states.
    """
    def inner(function):
        @functools.wraps(function)
        def wrapper(handler, message):
            if handler.state not in states:
                raise ValueError(f"Handler should be in one of the states in {states}, not {handler.state}.")
            try:
                return function(handler, message)
            except Exception as e:
                return {"error": str(e)}
        _actions[name] = wrapper
        return wrapper
    return inner

class Handler(socketserver.StreamRequestHandler):
    """
    A handler has a state associated with it, in order to perform authentication.
    Actions may change the .state attribute in order to change which actions are
    applicable. For example, an application might have a 'logged in' state, some
    actions which are only allowed when logged in, and a 'log in' action which
    transitions to the 'logged in' state.
    """
    def setup(self):
        super().setup()
        self.state = "start"
        logging.debug("New connection")
    def handle(self):
        while True:
            try:
                # I'd have liked to just read JSON from the socket, but the
                # Python JSON decoder complains about there being junk
                # after the document. So each message is its own line.
                # (If we want to send a newline, the encoder should
                # emit \n anyway.)
                message = json.loads(self.rfile.readline())
            except json.decoder.JSONDecodeError:
                return
            if message["name"] in _actions:
                response = _actions[message["name"]](self, message)
                self.wfile.write(json.dumps(response).encode() + b"\n")
                self.wfile.flush()
            else:
                return

class ReusingThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

def run(port):
    server = ReusingThreadingTCPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    finally:
        server.shutdown()
