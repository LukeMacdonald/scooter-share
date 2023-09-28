"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading, socket
from agent.web.app import create_agent_app
from master.web.app import create_master_app
from master.agent_interface.comms import run
from agent_common.socket_utils import recvJson, sendJson

PUBLIC_HOST = '0.0.0.0'
PRIVATE_HOST= '127.0.0.1'

def run_master():
    """
    Function to run the Flask master application.
    """
    master = create_master_app()
    master.run(host=PRIVATE_HOST, port=5000, debug=False, threaded=False)

def run_agent():
    """
    Function to run the Flask agent application.
    """
    agent = create_agent_app()
    agent.run(host=PUBLIC_HOST, port=5001, debug=False, threaded=True)

def run_socket(PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ADDRESS = (PUBLIC_HOST, PORT)
        s.bind(ADDRESS)
        s.listen()
        print("Listening on {}...".format(ADDRESS))
        while True:
            print("Waiting for Agent Pi...")
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                print()
                data = recvJson(conn)
                if "name" in data:
                    if data["name"] == "locations":
                        print("Looking for locations of all reported scooters")
                    elif data["name"] == "report-repair":
                        print("Engineering is reporting repair")
                    elif data['name'] == 'scooters-info':
                        print("Fetching all scooter information")     
                sendJson(conn, { "Message": data })
                    
if __name__ == '__main__':
    master_app = threading.Thread(target=run_master)
    agent_app = threading.Thread(target=run_agent)
    engineer_socket = threading.Thread(target=run_socket, args=(63000,)) 
    agent_app.start()
    master_app.start()
    engineer_socket.start()
