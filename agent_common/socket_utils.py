import socket
import json
import struct


PUBLIC_HOST = '0.0.0.0'
PRIVATE_HOST= '127.0.0.1'
MASTER_HOST = "192.168.1.98"
MASTER_PORT = 5000
AGENT_PORT = 5001
ENGINEER_SOCKET_PORT = 63000

def sendJson(socket, object):
    jsonString = json.dumps(object)
    data = jsonString.encode("utf-8")
    jsonLength = struct.pack("!i", len(data))
    socket.sendall(jsonLength)
    socket.sendall(data)

def recvJson(socket):
    buffer = socket.recv(4)
    jsonLength = struct.unpack("!i", buffer)[0]

    buffer = bytearray(jsonLength)
    view = memoryview(buffer)
    while jsonLength:
        nbytes = socket.recv_into(view, jsonLength)
        view = view[nbytes:]
        jsonLength -= nbytes

    jsonString = buffer.decode("utf-8")
    return json.loads(jsonString)