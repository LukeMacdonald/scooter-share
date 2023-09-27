import json
import socket

class Connection:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.rfile = self.socket.makefile("r")
    def send(self, message):
        self.socket.send(json.dumps(message).encode() + b"\n")
        line = self.rfile.readline()
        if line == "":
            raise EOFError
        else:
            return json.loads(line)
