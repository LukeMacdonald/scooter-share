"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
import socket
import logging
from agent.web.app import create_agent_app
from agent_common import socket_utils
from master.web.app import create_master_app
from master.agent_interface.engineer import fetch_engineer_data
from database.models import UserType

def run_master():
    """
    Function to run the master pi Flask application.
     - Needs to run on host 127.0.0.1 to ensure admin can only log onto site 
       from the physical master pi device
    """
    master = create_master_app()
    master.run(host=socket_utils.PRIVATE_HOST, port=socket_utils.MASTER_PORT, debug=False, threaded=False)

def run_agent():
    """
    Function to run the agent pi Flask application.
    """
    agent = create_agent_app()
    agent.run(host=socket_utils.PUBLIC_HOST, port=socket_utils.AGENT_PORT, debug=False, threaded=True)

def communicate_with_agent(port, user_type):
    """
    Function to run a socket server for communication between master and agent.
     - Temp function until learn how to integrate with handler
    
    Args:
        PORT (int): The port number for the socket server.
        USER_TYPE (str): The type of user (e.g., 'engineer' or 'customer').
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        address = (socket_utils.PUBLIC_HOST, port)
        s.bind(address)
        s.listen()
        print(f"Master Pi listening on port {port}...")
        while True:
            conn, addr = s.accept()
            print(f"Connected to: {addr}")
            with conn:
                data = socket_utils.recvJson(conn)
                if "name" in data:
                    if user_type == UserType.ENGINEER.value: 
                        response = fetch_engineer_data(data["name"],data)
                    elif user_type == UserType.CUSTOMER.value:
                        pass
                    else:
                        pass
                socket_utils.sendJson(conn, response)
            print("Connection Disconnected")
                    
if __name__ == '__main__':
    master_app = threading.Thread(target=run_master)
    master_app.start()
    
    agent_app = threading.Thread(target=run_agent)
    agent_app.start()
    
    engineer_socket = threading.Thread(target=communicate_with_agent, args=(socket_utils.ENGINEER_SOCKET_PORT,UserType.ENGINEER.value,))
    engineer_socket.start()
