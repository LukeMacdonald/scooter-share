"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
from agent.web.app import create_agent_app
from master.web.app import create_master_app
from master.agent_interface.app import run_agent_server

def run_master(master):
    "Run the Flask master application."
    master.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

def run_agent():
    "Function to run the Flask agent application."
    agent = create_agent_app()
    agent.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
    app = create_master_app()
    master_thread = threading.Thread(target=run_master, args=(app,))
    master_thread.start()
    agent_thread = threading.Thread(target=run_agent)
    agent_thread.start()
    agent_server_thread = threading.Thread(target=run_agent_server, args=(app,))
    agent_server_thread.start()
