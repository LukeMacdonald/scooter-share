"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
import socket
from agent.web.app import create_agent_app
from agent_common.socket_utils import recvJson, sendJson
from master.web.app import create_master_app
from master.agent_interface.engineer import fetchEngineerData

PUBLIC_HOST = '0.0.0.0'
PRIVATE_HOST= '127.0.0.1'
MASTER_PORT = 5000
AGENT_PORT = 5001
ENGINEER_SOCKET_PORT = 63000

def run_master():
    """
    Function to run the Flask master application.
    """
    master = create_master_app()
    master.run(host=PRIVATE_HOST, port=MASTER_PORT, debug=False, threaded=False)

def run_agent():
    """
    Function to run the Flask agent application.
    """
    agent = create_agent_app()
    agent.run(host=PUBLIC_HOST, port=AGENT_PORT, debug=False, threaded=True)

def run_socket(port, user_type):
    """
    Function to run a socket server for communication between master and agent.
    
    Args:
        PORT (int): The port number for the socket server.
        USER_TYPE (str): The type of user (e.g., 'engineer' or 'customer').
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        address = (PUBLIC_HOST, port)
        s.bind(address)
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Receiving connection from: {addr}")
                data = recvJson(conn)
                if "name" in data:
                    if user_type == "engineer":
                        response = fetchEngineerData(data["name"],data)
                    elif user_type == "customer":
                        pass
                    else:
                        pass
                sendJson(conn, response)
                    
if __name__ == '__main__':
    master_app = threading.Thread(target=run_master)
    master_app.start()
    agent_app = threading.Thread(target=run_agent)
    agent_app.start()
    engineer_socket = threading.Thread(target=run_socket, args=(ENGINEER_SOCKET_PORT,'engineer',))
    engineer_socket.start()
