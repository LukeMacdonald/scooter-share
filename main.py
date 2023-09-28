"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
from agent.web.app import create_agent_app
from master.web.app import create_master_app
from master.agent_interface.app import run_agent_server

def run_master():
    "Run the Flask master application."
    master = create_master_app()
    master.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

def run_agent():
    "Function to run the Flask agent application."
    agent = create_agent_app()
    agent.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
    master_app = threading.Thread(target=run_master)
    master_app.start()
    agent_app = threading.Thread(target=run_agent)
    agent_app.start()
    agent_server = threading.Thread(target=run_agent_server)
    agent_server.start()
