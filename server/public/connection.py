from common import comms, socket_utils

# Connect the first time that we use a connection.
conn = None
def get_connection() -> comms.Connection:
    global conn
    if conn is None:
        conn = comms.Connection(socket_utils.PRIVATE_HOST, socket_utils.SOCKET_PORT)
    return conn