"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
from agent.web.app import create_agent_app
from agent_common import socket_utils
from master.web.app import create_master_app
from master.agent_interface.app import run_agent_server

def run_master(master):
    "Run the Flask master application."
    master.run(host=socket_utils.PRIVATE_HOST, port=socket_utils.MASTER_PORT, debug=False, threaded=True)

def run_agent():
    "Function to run the Flask agent application."
    agent = create_agent_app()
    agent.run(host=socket_utils.PUBLIC_HOST, ssl_context=('cert.pem', 'key.pem'),port=socket_utils.AGENT_PORT, debug=False, threaded=True)               
if __name__ == '__main__':
    app = create_master_app()
    master_thread = threading.Thread(target=run_master, args=(app,))
    master_thread.start()
    agent_thread = threading.Thread(target=run_agent)
    agent_thread.start()
    agent_server_thread = threading.Thread(target=run_agent_server, args=(app,))
    agent_server_thread.start()
