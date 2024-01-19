"""
Main Module for Running Flask Master and Agent Applications in Separate Threads.
"""
import threading
from web.app import create_master_app
from comms.server import Server
from constants import PUBLIC_HOST, MASTER_PORT


def run_master(master):
    "Run the Flask master application."
    master.run(host=PUBLIC_HOST, port=MASTER_PORT, debug=False, threaded=True)


if __name__ == '__main__':
    server = Server("127.0.0.1", 54321)

    app = create_master_app()
    master_thread = threading.Thread(target=run_master, args=(app,))
    master_thread.start()
    agent_server_thread = threading.Thread(target=server.start_server, args=(app,))
    agent_server_thread.start()
